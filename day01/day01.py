def parse_input(input_file: str = "day1/input.txt") -> list:
    """Parse the txt puzzle input into a list of ints.

    Args:
        input_file (str, optional): Puzzle input txt file. Defaults to "day1/input.txt".

    Returns:
        list: Puzzle input as a list of ints.
    """
    o = open(input_file)
    output = [int(i.strip()) for i in o.readlines()]
    return output


def part_1(depth_measurements: list) -> int:
    """Count the number of times the depth measurement increases.

    Args:
        depth_measurements (list): Puzzle input.

    Returns:
        int: Number of depth increases.
    """
    current_depth = depth_measurements[0]
    depth_increases = 0
    for i in depth_measurements:
        if i > current_depth:
            depth_increases += 1
        current_depth = i
    return depth_increases


def part_2(depth_measurements: list, sliding_window: int = 3) -> int:
    """Count the number of times the depth measurement increases
    when constrained by a sliding window.

    Args:
        depth_measurements (list): Puzzle input.
        sliding_window (int, optional): Sliding window to consider. Defaults to 3.

    Returns:
        int: Number of depth increases.
    """
    current_window = sum(depth_measurements[0:sliding_window])
    depth_increases = 0
    for i in range(len(depth_measurements) - sliding_window + 1):
        window = sum(depth_measurements[i : i + sliding_window])
        if window > current_window:
            depth_increases += 1
        current_window = window
    return depth_increases


# Tests


def test_parse_input():
    output = parse_input("day01/input.txt")
    assert type(output) is list
    assert all(type(i) is int for i in output)


def test_part_1():
    output = parse_input("day01/example.txt")
    answer = part_1(output)
    assert answer == 7


def test_part_2():
    output = parse_input("day01/example.txt")
    answer = part_2(output)
    assert answer == 5


if __name__ == "__main__":
    output = parse_input("day01/input.txt")
    answer_1 = part_1(output)
    answer_2 = part_2(output)
    print("Day 1 Solutions:")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")
