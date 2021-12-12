class Cave:
    def __init__(self, height_map: list) -> None:
        """Cave with height map.

        Args:
            height_map (list): Height map of cave.
        """
        self.height_map = height_map
        self.len_x = len(self.height_map[0])
        self.len_y = len(self.height_map)
        self.max_x = self.len_x - 1
        self.max_y = self.len_y - 1

    def height(self, x: int, y: int) -> int:
        """Get the height of the given point.

        Args:
            x (int): x position.
            y (int): y position.

        Returns:
            int: Height of x, y.
        """
        return self.height_map[y][x]

    def get_neighbours(self, x: int, y: int) -> list:
        """Get the neighbours of the given position.

        Args:
            x (int): x position.
            y (int): y position.

        Returns:
            list: Neighbours of x, y.
        """
        neighbours = []
        if x != 0:
            neighbours.append((x - 1, y))
        if x < self.max_x:
            neighbours.append((x + 1, y))
        if y != 0:
            neighbours.append((x, y - 1))
        if y < self.max_y:
            neighbours.append((x, y + 1))
        return neighbours

    def is_low_point(self, x: int, y: int) -> bool:
        """Determine if position is a low point.

        Args:
            x (int): x position.
            y (int): y position.

        Returns:
            bool: True if position is a low point.
        """
        neighbours = self.get_neighbours(x, y)
        n_heights = [self.height(x_n, y_n) for x_n, y_n in neighbours]
        if all(h > self.height(x, y) for h in n_heights):
            return True
        else:
            return False

    def calculate_risk_level(self) -> int:
        """Calculate risk level.

        Returns:
            int: Risk level.
        """
        score = 0
        for y in range(self.len_y):
            for x in range(self.len_x):
                if self.is_low_point(x, y):
                    score += 1 + self.height(x, y)
        return score

    def basin_size(self, x: int, y: int) -> int:
        """Determine the basin size of the position.

        Args:
            x (int): x position.
            y (int): y position.

        Returns:
            int: Basin size.
        """
        stack = [(x, y)]
        visited = set([(x, y)])
        while stack:
            x_i, y_i = stack.pop()
            height_i = self.height(x_i, y_i)
            neighbours = self.get_neighbours(x_i, y_i)
            for n in neighbours:
                x_n, y_n = n
                height_n = self.height(x_n, y_n)
                if height_n > height_i and height_n < 9 and (x_n, y_n) not in visited:
                    stack.append((x_n, y_n))
                    visited.add((x_n, y_n))
        return len(visited)

    def part_2(self) -> int:
        """Solve part 2.

        Returns:
            int: Top 3 basin sizes multiplied together.
        """
        basins = []
        for y in range(self.len_y):
            for x in range(self.len_x):
                if self.is_low_point(x, y):
                    basins.append(self.basin_size(x, y))
        basins.sort()
        return basins[-3] * basins[-2] * basins[-1]


def parse_input(input_file: str) -> list:
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


def test_parse_input():
    output = parse_input("day9/example.txt")
    assert type(output) is list
    assert all(type(i) is list for i in output)
    for i in output:
        assert all(type(num) is int for num in i)


def test_is_low_point():
    grid = parse_input("day9/example.txt")
    cave = Cave(grid)
    assert cave.is_low_point(1, 0)
    assert cave.is_low_point(9, 0)
    assert cave.is_low_point(2, 2)
    assert cave.is_low_point(6, 4)

    assert not cave.is_low_point(5, 0)
    assert not cave.is_low_point(0, 0)
    assert not cave.is_low_point(9, 4)


def test_part_1():
    output = parse_input("day9/example.txt")
    cave = Cave(output)
    assert cave.calculate_risk_level() == 15


def test_basin_size():
    grid = parse_input("day9/example.txt")
    cave = Cave(grid)
    assert cave.basin_size(1, 0) == 3
    assert cave.basin_size(9, 0) == 9
    assert cave.basin_size(2, 2) == 14
    assert cave.basin_size(6, 4) == 9


def test_part_2():
    output = parse_input("day9/example.txt")
    cave = Cave(output)
    assert cave.part_2() == 1134


if __name__ == "__main__":
    output = parse_input("day9/input.txt")
    cave = Cave(output)
    answer_1 = cave.calculate_risk_level()
    answer_2 = cave.part_2()

    print("Day 9 Solutions:")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")
