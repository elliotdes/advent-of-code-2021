def command_to_xy(command: str) -> tuple:
    """Convert a command to x, y coordinates.

    Args:
        command (str): Command to convert.

    Returns:
        tuple: x, y coordinates of command.
    """
    direction, value = command.split()
    value = int(value)
    if direction == "forward":
        return (value, 0)
    elif direction == "down":
        return (0, value)
    elif direction == "up":
        return (0, -value)


def parse_input(input_file: str) -> list:
    """Parse the txt puzzle input.

    Args:
        input_file (str): Puzzle imput txt file.

    Returns:
        list: Parsed puzzle input.
    """
    o = open(input_file)
    output = [command_to_xy(i.strip()) for i in o.readlines()]
    return output


def part_1(commands: list) -> int:
    """Solve part 1.

    Args:
        commands (list): List of commands. Puzzle input.

    Returns:
        int: Horizontal position multiplied by the depth.
    """
    x_pos = sum([x for x, _ in commands])
    y_pos = sum([y for _, y in commands])
    return x_pos * y_pos


def part_2(commands: list) -> int:
    """Solve part 2. Accounts for aim.

    Args:
        commands (list): List of commands. Puzzle input.

    Returns:
        int: Horizontal position multiplied by the depth.
    """
    aim = 0
    x_pos = 0
    y_pos = 0
    for i in commands:
        x_pos += i[0]
        aim += i[1]
        y_pos += i[0] * aim
    return x_pos * y_pos


# Tests


def test_parse_input():
    output = parse_input("day2/example.txt")
    assert type(output) is list
    assert all(type(i) is tuple for i in output)


def test_part_1():
    output = parse_input("day2/example.txt")
    answer = part_1(output)
    assert answer == 150


def test_part_2():
    output = parse_input("day2/example.txt")
    answer = part_2(output)
    assert answer == 900


if __name__ == "__main__":
    output = parse_input("day2/input.txt")
    answer_1 = part_1(output)
    answer_2 = part_2(output)

    print("Day 2 Solutions:")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")
