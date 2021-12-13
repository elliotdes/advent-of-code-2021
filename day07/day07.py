def parse_input(input_file: str) -> list:
    """Parse the txt puzzle input.

    Args:
        input_file (str): Puzzle imput txt file.

    Returns:
        list: Parsed puzzle input.
    """
    o = open(input_file)
    output = o.readline().strip().split(",")
    output = [int(i) for i in output]
    return output


def min_fuel_median(crabs: list) -> int:
    """Find the minimum fuel cost when the target is the median.
    Optimality property.

    Args:
        crabs (list): Crabs initial positions.

    Returns:
        int: Minimum fuel cost.
    """
    crabs.sort()
    median = crabs[(len(crabs) - 1) // 2]
    fuel_cost = sum([abs(i - median) for i in crabs])
    return fuel_cost


def triangular_number(n: int) -> int:
    """Calculate the nth triangle number.

    Args:
        n (int): n.

    Returns:
        int: Triangle number.
    """
    return int(n * (n + 1) / 2)


def min_fuel_mean(crabs: list) -> int:
    """Find the minimum fuel cost when the target is the mean.

    Args:
        crabs (list): Crabs initial positions.

    Returns:
        int: Minimum fuel cost.
    """
    mean = round(sum(crabs) / len(crabs))
    mean_pos = mean + 1
    mean_neg = mean - 1
    fuel_cost = sum([triangular_number(abs(i - mean)) for i in crabs])
    fuel_cost_pos = sum([triangular_number(abs(i - mean_pos)) for i in crabs])
    fuel_cost_neg = sum([triangular_number(abs(i - mean_neg)) for i in crabs])
    return min(fuel_cost, fuel_cost_pos, fuel_cost_neg)


# Tests


def test_parse_input():
    output = parse_input("day07/example.txt")
    assert type(output) is list
    assert all(type(i) is int for i in output)


def test_part_1():
    output = parse_input("day07/example.txt")
    fuel_cost = min_fuel_median(output)
    assert fuel_cost == 37


def test_triangular_numbers():
    assert triangular_number(1) == 1
    assert triangular_number(2) == 3
    assert triangular_number(3) == 6
    assert triangular_number(4) == 10


def test_part_2():
    output = parse_input("day07/example.txt")
    fuel_cost = min_fuel_mean(output)
    assert fuel_cost == 168


if __name__ == "__main__":
    output = parse_input("day07/input.txt")
    answer_1 = min_fuel_median(output)
    answer_2 = min_fuel_mean(output)

    print("Day 7 Solutions:")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")
