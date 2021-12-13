from collections import defaultdict


def parse_input(input_file: str) -> list:
    """Parse the txt puzzle input.

    Args:
        input_file (str): Puzzle imput txt file.

    Returns:
        list: Parsed puzzle input.
    """
    output = []
    for line in open(input_file).readlines():
        line = line.strip()
        line = line.split(" -> ")
        line = [i.split(",") for i in line]
        line = [(int(i[0]), int(i[1])) for i in line]
        output.append(line)
    return output


def non_diagonal(xy1: tuple, xy2: tuple) -> bool:
    """Determine if two coordinates are non-diagonal to each other.

    Args:
        xy1 (tuple): Coordinate 1.
        xy2 (tuple): Coordinate 2.

    Returns:
        bool: if points are non-diagonal, return True.
    """
    if xy1[0] == xy2[0] or xy1[1] == xy2[1]:
        return True
    else:
        return False


def perfect_diagonal(xy1: tuple, xy2: tuple) -> bool:
    """Determine if two coordinates are 45° to each other.

    Args:
        xy1 (tuple): Coordinate 1.
        xy2 (tuple): Coordinate 2.

    Returns:
        bool: if points are 45° to each other, return True.
    """
    m = (xy2[1] - xy1[1]) / (xy2[0] - xy1[0])
    if abs(m) == 1:
        return True
    else:
        return False


def interpolate(xy1: tuple, xy2: tuple) -> set:
    """Interpolate points between two coordinates.

    Args:
        xy1 (tuple): Coordinate 1.
        xy2 (tuple): Coordinate 2.

    Returns:
        set: The coordinates between the two points.
    """
    covered_points = {xy1, xy2}
    x_min = min(xy1[0], xy2[0])
    x_max = max(xy1[0], xy2[0])
    y_min = min(xy1[1], xy2[1])
    y_max = max(xy1[1], xy2[1])
    if xy1[0] - xy2[0] == 0:  # Vertical line

        for y in range(y_min + 1, y_max):
            covered_points.add((x_max, y))
    else:
        m = (xy2[1] - xy1[1]) / (xy2[0] - xy1[0])
        c = xy1[1] - m * xy1[0]
        fy = lambda x: m * x + c

        for x in range(x_min + 1, x_max):
            covered_points.add((x, fy(x)))

    return covered_points


class VentGrid:
    def __init__(self) -> None:
        """Vent grid."""
        self.grid = defaultdict(int)

    def add_points(self, points: set) -> None:
        """Add points to grid.

        Args:
            points (set): The points to increment.
        """
        for point in points:
            self.grid[point] += 1

    def add_line(self, xy1: tuple, xy2: tuple) -> None:
        """Add line to grid.

        Args:
            xy1 (tuple): Coordinate 1.
            xy2 (tuple): Coordinate 2.
        """
        points = interpolate(xy1, xy2)
        self.add_points(points)

    def total_overlapping(self):
        count = 0
        for v in self.grid.values():
            if v > 1:
                count += 1
        return count


def part_1(lines: list) -> int:
    """Solve part 1.

    Args:
        lines (list): List of lines.

    Returns:
        int: Number of overlapping lines in vent grid.
    """
    grid = VentGrid()
    for line in lines:
        if non_diagonal(line[0], line[1]):
            grid.add_line(line[0], line[1])
    return grid.total_overlapping()


def part_2(lines: list) -> int:
    """Solve part 2. Same as part 2, but with 45° lines.

    Args:
        lines (list): List of lines.

    Returns:
        int: Number of overlapping lines in vent grid.
    """
    grid = VentGrid()
    for line in lines:
        if non_diagonal(line[0], line[1]) or perfect_diagonal(line[0], line[1]):
            grid.add_line(line[0], line[1])
    return grid.total_overlapping()


# Tests


def test_parse_input():
    output = parse_input("day05/example.txt")
    assert type(output) is list
    for coords in output:
        assert all(type(i) is tuple for i in coords)


def test_non_diagonal():
    assert non_diagonal((1, 1), (1, 3))
    assert not non_diagonal((0, 0), (8, 8))


def test_interpolate_line():
    line_1 = interpolate((1, 1), (1, 3))
    line_2 = interpolate((9, 7), (7, 7))
    assert line_1 == {(1, 1), (1, 2), (1, 3)}
    assert line_2 == {(9, 7), (8, 7), (7, 7)}


def test_part_1():
    output = parse_input("day05/example.txt")
    answer = part_1(output)
    assert answer == 5


def test_interpolate_diag():
    diag_1 = interpolate((1, 1), (3, 3))
    diag_2 = interpolate((9, 7), (7, 9))
    assert diag_1 == {(1, 1), (2, 2), (3, 3)}
    assert diag_2 == {(9, 7), (8, 8), (7, 9)}


def test_part_2():
    output = parse_input("day05/example.txt")
    answer = part_2(output)
    assert answer == 12


if __name__ == "__main__":
    output = parse_input("day05/input.txt")
    answer_1 = part_1(output)
    answer_2 = part_2(output)

    print("Day 5 Solutions:")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")
