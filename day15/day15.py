class Cavern:
    def __init__(self, grid: list) -> None:
        self.len_x = len(grid[0])
        self.len_y = len(grid)
        self.max_x = self.len_x - 1
        self.max_y = self.len_y - 1
        self.grid = grid_list_to_dict(grid)

    def min_node(self, not_visited: set, cost: dict) -> tuple:
        nv = list(not_visited)
        node = nv[0]
        for i in not_visited:
            if cost[i] < cost[node]:
                node = i
        return node

    def risk(self, xy: tuple) -> int:
        return self.grid[xy]

    def get_neighbours(self, xy: tuple) -> list:
        """Get the neighbours of the given position.

        Args:
            xy (tuple): x-y coordinates.

        Returns:
            list: Neighbours of x, y.
        """
        x, y = xy
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

    def minimum_path(self, xy: tuple) -> int:
        """Djikstras.

        Args:
            xy (tuple): [description]

        Returns:
            int: [description]
        """
        cost = dict.fromkeys(self.grid.keys(), float("infinity"))
        cost[(0, 0)] = 0
        not_visited = set(self.grid.keys())
        while not_visited:
            node = self.min_node(not_visited, cost)
            not_visited.remove(node)
            neighbours = [n for n in self.get_neighbours(node) if n in not_visited]
            for n in neighbours:
                new_cost = cost[node] + self.risk(n)
                if new_cost < cost[n]:
                    cost[n] = new_cost

        return cost[xy]

    def enlarge_cavern(self, n: int) -> dict:
        coords = list(self.grid.keys())
        for x, y in coords:
            for x_diff, x_i in enumerate(range(x, x + self.len_x * n, self.len_x)):
                for y_diff, y_i in enumerate(range(y, y + self.len_y * n, self.len_y)):
                    diff = x_diff + y_diff
                    self.grid[(x_i, y_i)] = self.grid[(x, y)] + diff
                    if self.grid[(x_i, y_i)] > 9:
                        self.grid[(x_i, y_i)] = self.grid[(x_i, y_i)] % 9
        self.len_x = self.len_x * n
        self.len_y = self.len_y * n
        self.max_x = self.len_x - 1
        self.max_y = self.len_y - 1

    def minimum_path_recursion(self, x: int, y: int) -> int:
        if x == 0 and y == 0:
            return 0
        else:
            neighbours = self.get_neighbours((x, y))
            return min(
                [self.minimum_path((n_x, n_y)) for n_x, n_y in neighbours]
            ) + self.risk((x, y))


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


def grid_list_to_dict(grid: list) -> dict:
    grid_dict = {}
    for y, row in enumerate(grid):
        for x, risk in enumerate(row):
            grid_dict[(x, y)] = risk
    return grid_dict


def part_1():
    ...


def part_2():
    ...


# Tests


def test_parse_input():
    output = parse_input("day15/example1.txt")
    assert type(output) is list
    assert all(type(i) is list for i in output)
    for i in output:
        assert all(type(num) is int for num in i)


def test_grid_dict():
    output = parse_input("day15/example1.txt")
    grid = grid_list_to_dict(output)
    assert type(grid) is dict
    assert grid[(8, 9)] == 8


def test_part_1():
    output = parse_input("day15/example1.txt")
    cavern = Cavern(output)
    assert cavern.minimum_path((0, 2)) == 3
    assert cavern.minimum_path((cavern.max_x, cavern.max_y)) == 40


def test_enlarge_grid():
    output = parse_input("day15/example1.txt")
    cavern = Cavern(output)
    cavern.enlarge_cavern(5)
    expected_output = parse_input("day15/example2.txt")
    expected_cavern = Cavern(expected_output)
    assert len(cavern.grid) == len(expected_cavern.grid)
    assert cavern.grid.keys() == expected_cavern.grid.keys()
    assert cavern.grid == expected_cavern.grid
    assert cavern.len_x == expected_cavern.len_x
    assert cavern.len_y == expected_cavern.len_y
    assert cavern.max_x == expected_cavern.max_x
    assert cavern.max_y == expected_cavern.max_y


def test_part_2():
    ...


if __name__ == "__main__":
    output = parse_input("day15/input.txt")
    cavern = Cavern(output)
    answer_1 = cavern.minimum_path((cavern.max_x, cavern.max_y))
    cavern.enlarge_cavern(5)
    answer_2 = cavern.minimum_path((cavern.max_x, cavern.max_y))

    print("Day 15 Solutions:")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")
