from collections import Counter


def parse_input(input_file: str) -> tuple[str, dict]:
    """Parse puzzle input.

    Args:
        input_file (str): Puzzle input txt file.

    Returns:
        tuple[str, dict]: Polymer and the rules.
    """
    o = open(input_file)
    polymer = o.readline().strip()
    o.readline()
    rules = [i.strip().split(" -> ") for i in o.readlines()]
    rules = {(i[0][0], i[0][1]): i[1] for i in rules}
    return polymer, rules


def evolve_polymer(polymer: str, rules: dict, step: int) -> int:
    """Evolve a polymer using given rules for a number of steps.

    Args:
        polymer (str): Initial polymer.
        rules (dict): Rules to follow.
        step (int): Steps to take.

    Returns:
        int: Solution.
    """
    elements = Counter(polymer)
    initial_pairs = [(polymer[i], polymer[i + 1]) for i in range(len(polymer) - 1)]
    current_gen = Counter(initial_pairs)

    for _ in range(step):
        next_gen = current_gen.copy()
        for pair in current_gen:
            if pair in rules:
                elements[rules[pair]] += current_gen[pair]
                next_gen[(pair[0], rules[pair])] += current_gen[pair]
                next_gen[(rules[pair], pair[1])] += current_gen[pair]
                next_gen[pair] -= current_gen[pair]
        current_gen = next_gen

    element_counts = sorted(elements.values())
    return element_counts[-1] - element_counts[0]


# Tests


def test_parse_input():
    polymer, rules = parse_input("day14/example.txt")
    assert type(polymer) is str
    assert type(rules) is dict


def test_part_1():
    polymer, rules = parse_input("day14/example.txt")
    answer = evolve_polymer(polymer, rules, 10)
    assert answer == 1588


def test_part_2():
    polymer, rules = parse_input("day14/example.txt")
    answer = evolve_polymer(polymer, rules, 40)
    assert answer == 2188189693529


if __name__ == "__main__":
    polymer, rules = parse_input("day14/input.txt")
    answer_1 = evolve_polymer(polymer, rules, 10)
    answer_2 = evolve_polymer(polymer, rules, 40)

    print("Day 14 Solutions:")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")
