from collections import defaultdict
from itertools import product
import re


def parse_input(input_file: str) -> list:
    """Parse puzzle input.

    Args:
        input_file (str): Input txt file.

    Returns:
        list: Commands.
    """
    o = open(input_file)
    commands = []
    for line in o.readlines():
        if line[:2] == "on":
            signal = 1
        else:
            signal = 0
        x1, x2, y1, y2, z1, z2 = map(int, re.findall("-?\d+", line))
        commands.append((signal, [x1, x2, y1, y2, z1, z2]))
    return commands


def part_1(commands: list, boundary=50) -> int:
    """Solve part 1.

    Args:
        commands (list): Puzzle commands.
        boundary (int, optional): Dimensional boundary. Defaults to 50.

    Returns:
        int: Number of cubes switched on.
    """
    grid = defaultdict(int)
    for signal, (x1, x2, y1, y2, z1, z2) in commands:
        x_range = range(max(x1, -boundary), min(x2, boundary) + 1)
        y_range = range(max(y1, -boundary), min(y2, boundary) + 1)
        z_range = range(max(z1, -boundary), min(z2, boundary) + 1)
        cubes = list(product(x_range, y_range, z_range))
        for cube in cubes:
            grid[cube] = signal

    return sum(grid.values())


def part_2():
    ...


# Tests


def test_parse_input():
    commands = parse_input("day22/example.txt")
    assert type(commands) == list
    assert all(type(sig) == int and type(coords) == list for sig, coords in commands)


def test_part_1():
    commands = parse_input("day22/example.txt")
    assert part_1(commands) == 590784


def test_part_2():
    ...


if __name__ == "__main__":
    output = parse_input("day22/input.txt")
    answer_1 = part_1(output)
    # answer_2 = part_2(output)

    print("Day 22 Solutions:")
    print(f"Part 1: {answer_1}")
    # print(f"Part 2: {answer_2}")
