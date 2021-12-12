class Octopi:
    def __init__(self, lights: list) -> None:
        """Map of octopi and their lights.

        Args:
            lights (list): Light levels of octopi.
        """
        self.lights = lights
        self.len_x = len(lights[0])
        self.len_y = len(lights)
        self.max_x = self.len_x - 1
        self.max_y = self.len_y - 1
        self.coords = set()
        for y in range(self.len_y):
            for x in range(self.len_x):
                self.coords.add((x, y))
        self.flash_count = 0

    def level(self, x: int, y: int) -> int:
        """Return the level of the octopi at that position.

        Args:
            x (int): x position.
            y (int): y position.

        Returns:
            int: Level of octopi.
        """
        return self.lights[y][x]

    def reset_level(self, x: int, y: int, value: int = 0) -> int:
        """Reset the level of the octopi at that position.

        Args:
            x (int): x position.
            y (int): y position.
            value (int, optional): Level to set octopi to. Defaults to 0.

        Returns:
            int: [description]
        """
        self.lights[y][x] = value

    def increment(self, x: int, y: int, for_zero: bool = True):
        """Increment the octopi at that position.

        Args:
            x (int): x position.
            y (int): y position.
            for_zero (bool, optional): If False, don't increment if octopi
            is at light level 0. Defaults to True.
        """
        if for_zero or self.level(x, y) != 0:
            self.lights[y][x] += 1

    def increment_all(self):
        """Increment all octopi."""
        for y in range(self.len_y):
            for x in range(self.len_x):
                self.increment(x, y)

    def get_neighbours(self, x: int, y: int) -> list:
        """Get all neighbours of the octopi at that position.

        Args:
            x (int): x position.
            y (int): y position.

        Returns:
            list: Neighbouring octopi.
        """
        potential_neighbours = [
            (x, y + 1),
            (x + 1, y + 1),
            (x + 1, y),
            (x + 1, y - 1),
            (x, y - 1),
            (x - 1, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
        ]
        neighbours = [n for n in potential_neighbours if n in self.coords]
        return neighbours

    def flash(self, x: int, y: int):
        """Flash the octopi at that position.

        Args:
            x (int): x position.
            y (int): y position.
        """
        self.flash_count += 1
        self.reset_level(x, y)
        for n in self.get_neighbours(x, y):
            x_n, y_n = n
            self.increment(x_n, y_n, for_zero=False)
            if 0 < self.level(x_n, y_n) >= 10:
                self.flash(x_n, y_n)

    def advance(self):
        """Advance one step."""
        self.increment_all()
        for y in range(self.len_y):
            for x in range(self.len_x):
                if self.level(x, y) >= 10:
                    self.flash(x, y)

    def part_1(self, steps: int = 100) -> int:
        """Solve part 1.

        Args:
            steps (int, optional): Number of steps to take. Defaults to 100.

        Returns:
            int: Number of total flashes.
        """
        for _ in range(steps):
            self.advance()
        return self.flash_count

    def all_flashed(self) -> bool:
        """Determine if all octopi have just flashed.

        Returns:
            bool: True if all octopi have just flashed.
        """
        return all(light == 0 for row in self.lights for light in row)

    def part_2(self) -> int:
        """Solve part 2.

        Returns:
            int: Turn when all octopi have flashed.
        """
        step = 0
        while not self.all_flashed():
            step += 1
            self.advance()
        return step


def parse_input(input_file: str):
    """Parse the txt puzzle input.

    Args:
        input_file (str): Puzzle imput txt file.

    Returns:
        list: Parsed puzzle input.
    """
    o = open(input_file)
    output = [i.strip() for i in o.readlines()]
    grid = []
    for i in output:
        row = [int(num) for num in i]
        grid.append(row)
    return grid


# Tests


def test_get_neighbours():
    output = parse_input("day11/example.txt")
    o = Octopi(output)
    assert set(o.get_neighbours(0, 0)) == set([(1, 0), (1, 1), (0, 1)])


def test_parse_input():
    output = parse_input("day11/example.txt")
    assert type(output) is list
    assert all(type(i) is list for i in output)
    for i in output:
        assert all(type(num) is int for num in i)


def test_part_1():
    output = parse_input("day11/example.txt")
    octo = Octopi(output)
    assert octo.part_1(10) == 204
    assert octo.part_1(90) == 1656  # 90 more steps


def test_part_2():
    output = parse_input("day11/example.txt")
    octo = Octopi(output)
    assert octo.part_2() == 195


if __name__ == "__main__":
    output = parse_input("day11/input.txt")
    octo_1 = Octopi(output)
    octo_2 = Octopi(output)
    answer_1 = octo_1.part_1(100)
    answer_2 = octo_2.part_2()

    print("Day 11 Solutions:")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")
