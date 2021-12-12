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


def opposite_bracket(
    bracket: str,
    open_brackets: list = ["(", "[", "{", "<"],
    close_brackets: list = [")", "]", "}", ">"],
) -> str:
    """Get the closing bracket for a given open bracket.

    Args:
        bracket (str): The open bracket to consider.
        open_brackets (list, optional): Open brackets to consider.
        Defaults to ["(", "[", "{", "<"].
        close_brackets (list, optional): Closed brackets to consider.
        Defaults to [")", "]", "}", ">"].

    Returns:
        str: The closing bracket of the supplied open bracket.
    """
    return close_brackets[open_brackets.index(bracket)]


def balanced_brackets(brackets: str) -> tuple:
    """Determine if brackets are balanced or not.

    Args:
        brackets (str): The string of brackets to consider.

    Returns:
        tuple: if brackets are balanced or not, and the remaining stack.
    """
    open_brackets = ["(", "[", "{", "<"]
    close_brackets = [")", "]", "}", ">"]
    stack = []
    for b in brackets:
        if b in open_brackets:
            stack.append(b)
        elif b in close_brackets:
            ob = opposite_bracket(stack[-1])
            if b == ob:
                stack.pop()
            else:
                return False, b
    completion_str = [opposite_bracket(i) for i in stack[::-1]]
    return True, "".join(completion_str)


def calculate_syntax_checker_score(subsystem: list) -> int:
    """Calculate syntax checker score of a subsytem.

    Args:
        subsystem (list): Subsystem to consider.

    Returns:
        int: Syntax checker score.
    """
    bracket_score = {")": 3, "]": 57, "}": 1197, ">": 25137}
    score = 0
    for chunk in subsystem:
        balanced, bracket = balanced_brackets(chunk)
        if not balanced:
            score += bracket_score[bracket]
    return score


def completion_str_score(completion_str: str) -> int:
    bracket_score = {")": 1, "]": 2, "}": 3, ">": 4}
    score = 0
    for bracket in completion_str:
        score *= 5
        score += bracket_score[bracket]
    return score


def calculate_autocomplete_score(subsytem: list) -> int:
    """Calculate auto-complete score of a subsytem.

    Args:
        subsystem (list): Subsystem to consider.

    Returns:
        int: Auto-complete score.
    """
    scores = []
    median = (len(subsytem) - 1) // 2
    for chunk in subsytem:
        balanced, brackets = balanced_brackets(chunk)
        if balanced:
            scores.append(completion_str_score(brackets))
    scores.sort()
    median = scores[(len(scores) - 1) // 2]
    return median


# Tests


def test_parse_input():
    output = parse_input("day10/example.txt")
    assert type(output) is list
    assert all(type(i) is str for i in output)


# Tests


def test_balance_brackets():
    assert balanced_brackets("(]") == (False, "]")
    assert balanced_brackets("{()()()>") == (False, ">")
    assert balanced_brackets("(((()))}") == (False, "}")
    assert balanced_brackets("<([]){()}[{}])") == (False, ")")


def test_part_1():
    output = parse_input("day10/example.txt")
    score = calculate_syntax_checker_score(output)
    assert score == 26397


def test_completion_str():
    assert balanced_brackets("[({(<(())[]>[[{[]{<()<>>") == (True, r"}}]])})]")
    assert balanced_brackets("(((({<>}<{<{<>}{[]{[]{}") == (True, r"}}>}>))))")
    assert balanced_brackets("{<[[]]>}<{[{[{[]{()[[[]") == (True, r"]]}}]}]}>")
    assert balanced_brackets("<{([{{}}[<[[[<>{}]]]>[]]") == (True, r"])}>")


def test_completion_str_score():
    assert completion_str_score(r"}}]])})]") == 288957
    assert completion_str_score(r")}>]})") == 5566
    assert completion_str_score(r"}}>}>))))") == 1480781
    assert completion_str_score(r"]]}}]}]}>") == 995444
    assert completion_str_score(r"])}>") == 294


def test_part_2():
    output = parse_input("day10/example.txt")
    score = calculate_autocomplete_score(output)
    assert score == 288957


if __name__ == "__main__":
    output = parse_input("day10/input.txt")
    answer_1 = calculate_syntax_checker_score(output)
    answer_2 = calculate_autocomplete_score(output)

    print("Day 10 Solutions:")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")
