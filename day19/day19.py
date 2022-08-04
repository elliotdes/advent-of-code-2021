from collections import defaultdict, Counter
from itertools import combinations, product


def parse_input(input_file: str) -> list:
    """Parse puzzle input.

    Args:
        input_file (str): Input txt file.

    Returns:
        list: Liat of scanner objects.
    """
    o = open(input_file)
    scanners = []
    for line in o.readlines():
        if line.startswith("---"):
            beacons = []
        elif line == "\n":
            scanners.append(beacons)
        else:
            beacons.append(tuple([int(i) for i in line.strip().split(",")]))

    # Append last set of beacons
    scanners.append(beacons)

    # Convert to Scanner objects
    scanner_objs = []
    for i in range(len(scanners)):
        scanner = Scanner(i, scanners[i])
        scanner_objs.append(scanner)
    return scanner_objs


class Scanner:
    def __init__(self, scanner_id: int, beacons: list) -> None:
        """Scanner object.

        Args:
            scanner_id (int): ID of scanner.
            beacons (list): Beacons within scanner.
        """
        self.id = scanner_id

        self.beacons = defaultdict(Counter)
        beacon_pairs = combinations(beacons, 2)
        for b1, b2 in beacon_pairs:
            self.beacons[b1][(manahattan_distance(b1, b2))] += 1
            self.beacons[b2][(manahattan_distance(b2, b1))] += 1

        self.positions = set()
        if scanner_id == 0:
            self.positions.add((0, 0, 0))

    @property
    def max_md(self) -> int:
        """Max Manhattan distance between scanner and its beacons.

        Returns:
            int: Manhattan distance.
        """
        positon_pairs = combinations(self.positions, 2)
        mds = [manahattan_distance(p1, p2) for p1, p2 in positon_pairs]
        return max(mds)


def rotate_beacon(beacon: tuple, i: int) -> tuple:
    """Rotate a beacon by a rotation i.

    Args:
        beacon (tuple): Beacon to rotate.
        i (int): Rotation number.

    Returns:
        tuple: Rotated beacon.
    """
    x, y, z = beacon
    rotations = [
        (x, y, z),
        (z, y, -x),
        (-x, y, -z),
        (-z, y, x),
        (-x, -y, z),
        (-z, -y, -x),
        (x, -y, -z),
        (z, -y, x),
        (x, -z, y),
        (y, -z, -x),
        (-x, -z, -y),
        (-y, -z, x),
        (x, z, -y),
        (-y, z, -x),
        (-x, z, y),
        (y, z, x),
        (z, x, y),
        (y, x, -z),
        (-z, x, -y),
        (-y, x, z),
        (-z, -x, y),
        (y, -x, z),
        (z, -x, -y),
        (-y, -x, -z),
    ]
    return rotations[i]


def find_vector(beacon1: tuple, beacon2: tuple) -> tuple:
    """Find vector between two beacons.

    Args:
        beacon1 (tuple): Beacon 1.
        beacon2 (tuple): Beacon 2.

    Returns:
        tuple: Vector between the beacons.
    """
    x1, y1, z1 = beacon1
    x2, y2, z2 = beacon2
    return ((x2 - x1), (y2 - y1), (z2 - z1))


def add_vector(beacon1: tuple, beacon2: tuple) -> tuple:
    """Add the vectors of two beacons.

    Args:
        beacon1 (tuple): Beacon 1.
        beacon2 (tuple): Beacon 2.

    Returns:
        tuple: Resultant vector of the beacons.
    """
    x1, y1, z1 = beacon1
    x2, y2, z2 = beacon2
    return ((x1 + x2), (y1 + y2), (z1 + z2))


def manahattan_distance(beacon1: tuple, beacon2: tuple) -> int:
    """Manhattan distance between two beacons.

    Args:
        beacon1 (tuple): Beacon 1.
        beacon2 (tuple): Beacon 2.

    Returns:
        int: Manhattan distance.
    """
    x1, y1, z1 = beacon1
    x2, y2, z2 = beacon2
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


def get_overlapping(scanner1: Scanner, scanner2: Scanner, overlap_no: int = 11) -> bool:
    """Find if two scanners are overlapping.

    Args:
        scanner1 (Scanner): Scanner 1.
        scanner2 (Scanner): Scanner 2.
        overlap_no (int, optional): The minimum number of beacons that
        must be the same to consider the scanners overlapping.
        Defaults to 11.

    Returns:
        bool: If the scanners are overlapping or not.
    """

    overlapping_beacons = []
    beacon_pairs = product(scanner1.beacons, scanner2.beacons)

    for sb1, sb2 in beacon_pairs:
        md1 = scanner1.beacons[sb1]
        md2 = scanner2.beacons[sb2]
        overlapping_md = md1 & md2
        if sum(overlapping_md.values()) >= overlap_no:
            overlapping_beacons.append((sb1, sb2))

    return overlapping_beacons


def find_rotation(beacon_pair1: tuple[tuple], beacon_pair2: tuple[tuple]) -> int:
    """Find the rotation of one scanner relevant to another.

    Args:
        beacon_pair1 (tuple[tuple]): Scanner beacon pair 1.
        beacon_pair2 (tuple[tuple]): Scanner beacon pair 2.

    Raises:
        Exception: If no rotation is found.

    Returns:
        int: Rotation number.
    """
    vector_pair1 = (beacon_pair1[0], beacon_pair2[0])
    vector_pair2 = (beacon_pair1[1], beacon_pair2[1])
    v1 = find_vector(vector_pair1[0], vector_pair1[1])
    v2 = find_vector(vector_pair2[0], vector_pair2[1])
    for i in range(24):
        v2_rotated = rotate_beacon(v2, i)
        if v2_rotated == v1:
            return i
    raise Exception("No rotation found.")


def find_scanner_pos(beacon1: tuple, beacon2: tuple, rotate: int) -> tuple:
    """Find a scanners position relative to another scanner.

    Args:
        beacon1 (tuple): Beacon 1.
        beacon2 (tuple): Beacon 2.
        rotate (int): Rotation number.

    Returns:
        tuple: The relative scanner position.
    """
    beacon2 = rotate_beacon(beacon2, rotate)
    return find_vector(beacon2, beacon1)


def assemble_beacon_map(scanners: list[Scanner]) -> Scanner:
    """Assemble complete map of beacons.

    Args:
        scanners (list[Scanner]): List of scanners to consider.

    Returns:
        Scanner: Map of beacons on root scanner.
    """
    central_scanner = scanners.pop(0)
    while scanners:
        pot_scanner = scanners.pop(0)
        overlapping = get_overlapping(central_scanner, pot_scanner)
        match = len(overlapping) >= 11

        if match:
            beacon_pair1 = overlapping[0]
            beacon_pair2 = overlapping[1]
            rotation = find_rotation(beacon_pair1, beacon_pair2)
            beacon_s_central, beacon_s_pot = overlapping[0]
            pos_s_pot = find_scanner_pos(beacon_s_central, beacon_s_pot, rotation)
            central_scanner.positions.add(pos_s_pot)

            # add new beacons to central scanner, with relative
            for bs2 in pot_scanner.beacons:
                relative_pos = add_vector(pos_s_pot, rotate_beacon(bs2, rotation))
                central_scanner.beacons[relative_pos] += pot_scanner.beacons[bs2]

        else:
            scanners.append(pot_scanner)

    return central_scanner


# Tests


def test_parse_input():
    scanners = parse_input("day19/example.txt")
    assert type(scanners) == list
    assert all(type(i) == Scanner for i in scanners)


def test_overlapping_beacons():
    scanners = parse_input("day19/example.txt")
    o = get_overlapping(scanners[0], scanners[1])
    assert len(o) >= 11


def test_find_rotation():
    scanners = parse_input("day19/example.txt")
    o = get_overlapping(scanners[0], scanners[1])
    r = find_rotation(o[0], o[1])
    assert r == 2
    b1, b2 = o[0]
    assert find_scanner_pos(b1, b2, r) == (68, -1246, -43)


def test_part_1():
    scanners = parse_input("day19/example.txt")
    beacon_map = assemble_beacon_map(scanners)
    assert len(beacon_map.beacons) == 79


def test_part_2():
    scanners = parse_input("day19/example.txt")
    beacon_map = assemble_beacon_map(scanners)
    assert beacon_map.max_md == 3621


if __name__ == "__main__":
    output = parse_input("day19/input.txt")
    beacon_map = assemble_beacon_map(output)
    answer_1 = len(beacon_map.beacons)
    answer_2 = beacon_map.max_md

    print("Day 19 Solutions:")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")
