def transpose(array: list) -> list:
    """Transpose a list of strings.

    Args:
        array (list): List of strings.

    Returns:
        list: Transposed input.
    """
    return ["".join(i) for i in zip(*array)]


def parse_input(input_file: str) -> list:
    """Parse the txt puzzle input.

    Args:
        input_file (str): Puzzle imput txt file.

    Returns:
        list: Parsed puzzle input.
    """
    o = open(input_file)
    output = [i.strip() for i in o.readlines()]
    return output


def part_1(binary_numbers: list) -> int:
    """Solve part 1.

    Args:
        binary_numbers (list): List of binary numbers.

    Returns:
        int: Gamma multiplied by epsilon.
    """
    t_binary_numbers = transpose(binary_numbers)
    threshold = len(t_binary_numbers[0]) / 2
    gamma = ""
    epsilon = ""
    for i in t_binary_numbers:
        count = i.count("1")
        if count > threshold:
            gamma += "1"
            epsilon += "0"
        else:
            gamma += "0"
            epsilon += "1"
    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)
    return gamma * epsilon


def common_bit(binary_numbers: list, position: int, default_bit: str = "1") -> tuple:
    """Return the most common bit in that position in a list of binary numbers.

    Args:
        binary_numbers (list): List of binary numbers.
        position (int): Position to check.
        default_bit (str, optional): The bit to return if 1 is the most common.
        Defaults to "1".

    Returns:
        tuple: The most common bit and its opposite.
    """
    bits = [i[position] for i in binary_numbers]
    threshold = len(binary_numbers) / 2
    opposite_bit = str(1 - int(default_bit))
    if bits.count("1") >= threshold:
        return default_bit, opposite_bit
    else:
        return opposite_bit, default_bit


def part_1b(binary_numbers: list) -> int:
    """Solve part 1. Uses the common_bit function.

    Args:
        binary_numbers (list): List of binary numbers.

    Returns:
        int: Gamma multiplied by epsilon.
    """
    gamma = ""
    epsilon = ""

    bin_len = len(binary_numbers[0])
    for n in range(bin_len):
        gamma_bit, epsilon_bit = common_bit(binary_numbers, n)
        gamma += gamma_bit
        epsilon += epsilon_bit

    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)
    return gamma * epsilon


def bit_criteria_rating(binary_numbers: list, default_bit: str) -> int:
    """Returns the bit criteria rating.
    Either the oxygen generator or CO2 scrubber rating.

    Args:
        binary_numbers (list): List of binary numbers.
        default_bit (str): "1" for oxygen generator rating,
        "0" for CO2 scrubber rating.

    Returns:
        int: Criteria rating.
    """
    bin_len = len(binary_numbers[0])

    for n in range(bin_len):
        bit, _ = common_bit(binary_numbers, n, default_bit)
        binary_numbers = [bin_num for bin_num in binary_numbers if bin_num[n] == bit]

        if len(binary_numbers) == 1:
            return int(binary_numbers[0], 2)


def part_2(binary_numbers: list) -> int:
    """Solve part 2.

    Args:
        binary_numbers (list): List of binary numbers.

    Returns:
        int: Oxygen rating multiplied by CO2 rating.
    """
    o2_rating = bit_criteria_rating(binary_numbers, "1")
    co2_rating = bit_criteria_rating(binary_numbers, "0")
    return o2_rating * co2_rating


# Tests


def test_parse_input():
    output = parse_input("day3/example.txt")
    assert type(output) is list
    assert all(type(i) is str for i in output)


def test_part_1():
    output = parse_input("day3/example.txt")
    answer = part_1(output)
    assert answer == 198


def test_o2_generator_rating():
    output = parse_input("day3/example.txt")
    rating = bit_criteria_rating(output, "1")
    assert rating == 23


def test_co2_scrubber_rating():
    output = parse_input("day3/example.txt")
    rating = bit_criteria_rating(output, "0")
    assert rating == 10


def test_part_2():
    output = parse_input("day3/example.txt")
    answer = part_2(output)
    assert answer == 230


if __name__ == "__main__":
    output = parse_input("day3/input.txt")
    answer_1 = part_1(output)
    answer_1b = part_1b(output)
    answer_2 = part_2(output)

    print("Day 3 Solutions:")
    print(f"Part 1: {answer_1}")
    print(f"Part 1b: {answer_1b}")
    print(f"Part 2: {answer_2}")
