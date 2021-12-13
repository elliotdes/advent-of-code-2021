from collections import deque, defaultdict, Counter


class Graph:
    def __init__(self) -> None:
        """Undirected graph."""
        self.graph = defaultdict(list)

    def add_vertex(self, start: str, end: str) -> None:
        """Add vertex.

        Args:
            start (str): Start node.
            end (str): End node.
        """
        self.graph[start].append(end)
        self.graph[end].append(start)

    def all_paths(self, start: str, end: str) -> list:
        """Find all paths between start and end.
        Big caves can be revisted.

        Args:
            start (str): Start node.
            end (str): End node.

        Returns:
            list: Paths.
        """
        paths = []
        queue = deque()
        queue.append([start])
        while queue:
            path = queue.pop()
            node = path[-1]
            if node == end:
                paths.append(path)
            else:
                to_visit = [n for n in self.graph[node] if n not in path or n.isupper()]
                for i in to_visit:
                    queue.appendleft(path + [i])
        return paths

    def all_paths_with_small(self, start: str, end: str, max_revisits: int = 2) -> list:
        """Find all paths between start and end.
        Big caves can be revisited and
        a single small cave can be revisited max_revisits times.

        Args:
            start (str): Start node.
            end (str): End node.
            max_revisits (int, optional): Maximum number of times a
            small cave can be revisited. Defaults to 2.

        Returns:
            list: Paths.
        """
        paths = []
        queue = deque()
        queue.append([start])
        while queue:
            path = queue.pop()
            node = path[-1]
            if node == end:
                paths.append(path)
            else:
                small_caves = [cave for cave in path if cave.islower()]
                count = Counter(small_caves)
                revisits = max(count.values())
                to_visit = [
                    n
                    for n in self.graph[node]
                    if n not in path
                    or n.isupper()
                    or (n.islower() and revisits < max_revisits)
                    and (n != "start")
                ]
                for i in to_visit:
                    queue.appendleft(path + [i])
        return paths


def parse_input(input_file: str) -> list:
    """Parse the txt puzzle input.

    Args:
        input_file (str): Puzzle imput txt file.

    Returns:
        list: Parsed puzzle input.
    """
    o = open(input_file)
    output = [i.strip().split("-") for i in o.readlines()]
    return output


def part_1(rough_map: list) -> int:
    """Solve part 1.

    Args:
        rough_map (list): Puzzle input.

    Returns:
        int: Number of paths.
    """
    caves = Graph()
    for i in rough_map:
        caves.add_vertex(i[0], i[1])
    paths = caves.all_paths("start", "end")
    return len(paths)


def part_2(rough_map: list) -> int:
    """Solve part 2.

    Args:
        rough_map (list): Puzzle input.

    Returns:
        int: Number of paths.
    """
    caves = Graph()
    for i in rough_map:
        caves.add_vertex(i[0], i[1])
    paths = caves.all_paths_with_small("start", "end")
    return len(paths)


# Tests


def test_parse_input():
    output = parse_input("day12/example1.txt")
    assert type(output) is list
    assert all(type(i) is list for i in output)


def test_part_1():
    output1 = parse_input("day12/example1.txt")
    output2 = parse_input("day12/example2.txt")
    output3 = parse_input("day12/example3.txt")
    assert part_1(output1) == 10
    assert part_1(output2) == 19
    assert part_1(output3) == 226


def test_part_2():
    output1 = parse_input("day12/example1.txt")
    output2 = parse_input("day12/example2.txt")
    output3 = parse_input("day12/example3.txt")
    assert part_2(output1) == 36
    assert part_2(output2) == 103
    assert part_2(output3) == 3509


if __name__ == "__main__":
    output = parse_input("day12/input.txt")
    answer_1 = part_1(output)
    answer_2 = part_2(output)

    print("Day 12 Solutions:")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")
