def parse_input(input_file: str) -> list:
    """Parse puzzle input.

    Args:
        input_file (str): Puzzle input txt file.

    Returns:
        list: Initial lantern fish.
    """
    o = open(input_file)
    output = o.readline().strip().split(",")
    output = [int(i) for i in output]
    return output


def stimulate_fish(fish: list, days: int) -> int:
    """Stimulate fish for a given number of days.

    Args:
        fish (list): Fish to stimulate.
        days (int): Days to stimulate for.

    Returns:
        int: Total fish at end of stimulation period.
    """
    fish_clock = [fish.count(i) for i in range(9)]
    for _ in range(days):
        new_fish = fish_clock.pop(0)
        fish_clock[6] += new_fish
        fish_clock.append(new_fish)
        total_fish = sum(fish_clock)
    return total_fish


# Tests


def test_parse_input():
    output = parse_input("day06/example.txt")
    assert type(output) is list
    assert all(type(i) is int for i in output)


def test_part_1():
    output = parse_input("day06/example.txt")
    assert stimulate_fish(output, 18) == 26
    assert stimulate_fish(output, 80) == 5934


def test_part_2():
    output = parse_input("day06/example.txt")
    assert stimulate_fish(output, 256) == 26984457539


if __name__ == "__main__":
    output = parse_input("day06/input.txt")
    answer_1 = stimulate_fish(output, 80)
    answer_2 = stimulate_fish(output, 256)

    print("Day 6 Solutions:")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")
