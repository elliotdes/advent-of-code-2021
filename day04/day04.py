class Board:
    def __init__(self, bingo_card: list) -> None:
        """Bingo board.

        Args:
            bingo_card (list): Bingo card board.
        """
        self.lines = []
        t_bingo_card = [i for i in (zip(*bingo_card))]
        for row in bingo_card:
            self.lines.append(set(row))
        for col in t_bingo_card:
            self.lines.append(set(col))

        self.unmarked_numbers = set([i for row in bingo_card for i in row])
        self.called_numbers = set()

    def call_number(self, number: int) -> bool:
        """Call bingo number.

        Args:
            number (int): Number to call.

        Returns:
            bool: if bingo due to called number.
        """
        if number in self.unmarked_numbers:
            self.unmarked_numbers.remove(number)
        self.called_numbers.add(number)
        return self.bingo()

    def bingo(self) -> bool:
        """Determine if bingo has occurred.

        Returns:
            bool: Bingo occurrence.
        """
        for line in self.lines:
            if line < self.called_numbers:
                return True
        return False

    def calculate_score(self, called_number: int) -> int:
        """Calculate the score of the board at time of bingo.

        Args:
            called_number (int): The number called on.

        Returns:
            int: The score.
        """
        return sum(self.unmarked_numbers) * called_number


def parse_input(input_file: str) -> tuple:
    """Parse the txt puzzle input.

    Args:
        input_file (str): Puzzle imput txt file.

    Returns:
        tuple: The numbers to be called and the boards to play.
    """
    o = open(input_file)
    numbers = o.readline().strip().split(",")
    numbers = [int(num) for num in numbers]

    o.readline()
    board = []
    boards = []
    for i in o.readlines():
        if i == "\n":
            boards.append(board)
            board = []
        else:
            row = i.strip().split(" ")
            row = [int(num) for num in row if num != ""]
            board.append(row)

    # Append the last board
    boards.append(board)
    return numbers, boards


def part_1(numbers: list, boards: list) -> int:
    """Solve part 1.

    Args:
        numbers (list): The numbers to be called.
        boards (list): The boards to play.

    Returns:
        int: The score of the first winning board.
    """
    boards = [Board(board) for board in boards]
    for number in numbers:
        for board in boards:
            if board.call_number(number):
                return board.calculate_score(number)


def part_2(numbers: list, boards: list) -> int:
    """Solve part 2.

    Args:
        numbers (list): The numbers to be called.
        boards (list): The boards to play.

    Returns:
        int: The score of the last winning board.
    """
    boards = [Board(board) for board in boards]
    for number in numbers:
        if len(boards) > 1:
            boards = [board for board in boards if not board.call_number(number)]
        else:
            if boards[0].call_number(number):
                return boards[0].calculate_score(number)


# Tests


def test_parse_input():
    numbers, boards = parse_input("day04/example.txt")
    assert type(numbers) is list
    assert all(type(i) is int for i in numbers)
    assert len(boards) == 3
    for board in boards:
        assert all(len(i) == 5 for i in board)


def test_part_1():
    numbers, boards = parse_input("day04/example.txt")
    answer = part_1(numbers, boards)
    assert answer == 4512


def test_part_2():
    numbers, boards = parse_input("day04/example.txt")
    answer = part_2(numbers, boards)
    assert answer == 1924


if __name__ == "__main__":
    numbers, boards = parse_input("day04/input.txt")
    answer_1 = part_1(numbers, boards)
    answer_2 = part_2(numbers, boards)

    print("Day 4 Solutions:")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")
