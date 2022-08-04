def parse_input(input_file: str) -> list:
    """Parse puzzle input.

    Args:
        input_file (str): Input txt file.

    Returns:
        list: Puzzle input.
    """
    output = []
    for line in open(input_file).readlines():
        line = line.strip()
        line = line.split(" | ")
        line = [i.split() for i in line]
        output.append(line)
    return output


def part_1(entries: list) -> int:
    """Solve part 1.

    Args:
        entries (list): Puzzle entries.

    Returns:
        int: Unique digit appearences.
    """
    output = [entry[1] for entry in entries]
    unique_count = 0
    for vals in output:
        uniques = [len(val) in {2, 4, 3, 7} for val in vals]
        unique_count += sum(uniques)
    return unique_count


def solve_signal_pattern(signal_pattern: list) -> dict:
    """WIP. Solve signal patterns.

    Args:
        signal_pattern (list): Signal patterns.

    Returns:
        dict: Solved signal pattern.
    """
    # cdafg dage fgdaec cdbfgae cge gcbdfa fdceb gfceab ge ecfgd
    decoder = {set(i): None for i in signal_pattern}
    # decoder = {'cdafg': None, 'dage': None, ...}
    for i in signal_pattern:
        if len(i) == 2:
            decoder[i] = 1
        elif len(i) == 4:
            decoder[i] = 4
        elif len(i) == 3:
            decoder[i] = 7
        elif len(i) == 7:
            decoder[i] = 8

    signals = "abcdefg"
    signal_decoder = {i: None for i in signals}
    # signal_decoder = {'a': None, 'b': None, ...}
    flat_patterns = "".join(signal_pattern)
    signal_counts = {i: flat_patterns.count(i) for i in signals}
    # {'a': 8, 'b': 6, 'c': 8, 'd': 7, 'e': 4, 'f': 9, 'g': 7}
    for signal, count in signal_counts.items():
        if count == 4:
            signal_decoder["e"] = signal
        elif count == 6:
            signal_decoder["b"] = signal
        elif count == 9:
            signal_decoder["f"] = signal

    signal_decoder["a"] = "".join(decoder)

    return signal_counts


def part_2(entries: list) -> int:
    ...


# Tests


def test_parse_input():
    output = parse_input("day08/example.txt")
    assert type(output) is list
    for entry in output:
        assert len(entry[0]) == 10
        assert len(entry[1]) == 4


def test_part_1():
    output = parse_input("day08/example.txt")
    unique_count = part_1(output)
    assert unique_count == 26


def test_part_2():
    ...


if __name__ == "__main__":
    output = parse_input("day08/input.txt")
    answer_1 = part_1(output)

    print("Day 8 Solutions:")
    print(f"Part 1: {answer_1}")
