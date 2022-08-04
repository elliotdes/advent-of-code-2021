import functools
from itertools import product


def determined_dice():
    """Generator for the determined dice.

    Yields:
        Iterator[int]: Value of the dice.
    """
    while True:
        for i in range(1, 100 + 1):
            yield i


class Player:
    def __init__(self, position: int):
        """Player class.

        Args:
            position (int): Initial starting position.
        """
        self.positon = position
        self.score = 0

    def move(self, value: int):
        """Move the player.

        Args:
            value (int): Value to move player by.
        """
        self.positon += value
        self.positon %= 10
        if self.positon == 0:
            self.positon = 10
        self.score += self.positon

    def has_won(self, win_condition: int = 1000) -> bool:
        """Determine if the player has won.

        Args:
            win_condition (int, optional): Score required to win.
            Defaults to 1000.

        Returns:
            bool: If the player has won.
        """
        if self.score >= win_condition:
            return True
        else:
            return False


def part_1(position1: int, position2: int) -> int:
    """Solve part 1.

    Args:
        position1 (int): Initial positon of player 1.
        position2 (int): Initial position of player 2.

    Returns:
        int: Score of the losing player multiplied by the number of
        times the die was rolled during the game.
    """
    p1 = Player(position1)
    p2 = Player(position2)
    players = [p1, p2]
    dice = determined_dice()
    rolls = 0
    while True:
        for i in [0, 1]:
            die = next(dice), next(dice), next(dice)
            rolls += 3
            players[i].move(sum(die))
            if players[i].has_won():
                losing_player = players[i ^ 1]
                return losing_player.score * rolls


@functools.cache
def part_2(position1: int, position2: int, score1: int = 0, score2: int = 0) -> tuple:
    """Solve part 2.

    Args:
        position1 (int): Initial position of player 1.
        position2 (int): Initial position of player 2.
        score1 (int, optional): Score of player 1. Defaults to 0.
        score2 (int, optional): Score of player 2. Defaults to 0.

    Returns:
        tuple: Number of universe wins for each player.
    """
    if score1 >= 21:
        return 1, 0
    elif score2 >= 21:
        return 0, 1

    p1_wins = 0
    p2_wins = 0

    for die in product([1, 2, 3], [1, 2, 3], [1, 2, 3]):
        new_positon = (position1 + sum(die)) % 10
        if new_positon == 0:
            new_positon = 10
        new_score = score1 + new_positon

        w2, w1 = part_2(position2, new_positon, score2, new_score)

        p1_wins += w1
        p2_wins += w2

    return p1_wins, p2_wins


# Tests


def test_part_1():
    answer = part_1(4, 8)
    assert answer == 739785


def test_part_2():
    answer = part_2(4, 8)
    assert max(answer) == 444356092776315


if __name__ == "__main__":
    answer_1 = part_1(8, 3)
    answer_2 = max(part_2(8, 3))

    print("Day 21 Solutions:")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")
