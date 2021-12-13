from collections import defaultdict


class FoldingPaper:
    def __init__(self, dots: list) -> None:
        """Folding paper.

        Args:
            dots (list): Initial dots coordinates.
        """
        self.paper = defaultdict(int)
        for i in dots:
            self.paper[i] += 1

    def fold_x(self, line: int):
        """Fold along the x axis.

        Args:
            line (int): Line to fold against.
        """
        for x, y in list(self.paper):
            if x > line:
                new_line = 2 * line - x
                if new_line >= 0:
                    self.paper[(new_line, y)] += self.paper[(x, y)]
                    self.paper.pop((x, y))

    def fold_y(self, line: int):
        """Fold along the y axis.

        Args:
            line (int): Line to fold against.
        """
        for x, y in list(self.paper):
            if y > line:
                new_line = 2 * line - y
                if new_line >= 0:
                    self.paper[(x, new_line)] += self.paper[(x, y)]
                    self.paper.pop((x, y))

    @property
    def number_of_dots(self) -> int:
        """The number of dots on the folded paper.

        Returns:
            [int]: Number of dots.
        """
        return len(self.paper)


def parse_input(input_file: str) -> tuple:
    """Parse the txt puzzle input.

    Args:
        input_file (str): Puzzle imput txt file.

    Returns:
        tuple: Parsed puzzle input. Initial dots and the folds to make.
    """
    o = open(input_file)
    output = [i.strip().split(",") for i in o.readlines()]
    dots = [(int(i[0]), int(i[1])) for i in output if len(i) == 2]
    instructions = [i[0].split("=") for i in output if "fold" in i[0]]
    instructions = [(i[0][-1], int(i[1])) for i in instructions]
    return dots, instructions


def part_1(dots: list, instructions: list) -> int:
    """Solve part 1.

    Args:
        dots (list): Dots from puzzle input.
        instructions (list): Instructions from puzzle input.

    Returns:
        int: Number of dots after 1 fold.
    """
    paper = FoldingPaper(dots)
    axis, line = instructions[0]
    if axis == "x":
        paper.fold_x(line)
    elif axis == "y":
        paper.fold_y(line)
    return paper.number_of_dots


def part_2(dots: list, instructions: list) -> str:
    """Solve part 2.

    Args:
        dots (list): Dots from puzzle input.
        instructions (list): Instructions from puzzle input.

    Returns:
        str: Printable string of paper after all folds.
    """
    paper = FoldingPaper(dots)
    for axis, line in instructions:
        if axis == "x":
            paper.fold_x(line)
        elif axis == "y":
            paper.fold_y(line)
    return print_grid(paper.paper)


def print_grid(grid: dict) -> str:
    """Print coordinates inside a 2D matrix.

    Args:
        grid (dict): Coordinates.

    Returns:
        str: Printable string representation of matrix.
    """
    max_x = max(x for x, _ in grid) + 1
    max_y = max(y for _, y in grid) + 1
    matrix = [[" " for _ in range(max_x)] for _ in range(max_y)]
    for x, y in grid:
        matrix[y][x] = "█"
    printable_matrix = "\n".join(["".join(i) for i in matrix])
    return "\n" + printable_matrix


# Tests


def test_parse_input():
    dots, instructions = parse_input("day13/example.txt")
    assert type(dots) and type(instructions) is list


def test_part_1():
    dots, instructions = parse_input("day13/example.txt")
    answer = part_1(dots, instructions)
    assert answer == 17


if __name__ == "__main__":
    dots, instructions = parse_input("day13/input.txt")
    answer_1 = part_1(dots, instructions)
    answer_2 = part_2(dots, instructions)

    print("Day 13 Solutions:")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")
