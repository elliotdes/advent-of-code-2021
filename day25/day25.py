class Cucumbers:
    def __init__(self, grid: dict, regions: dict, max_x: int, max_y: int) -> None:
        """Sea cucumbers.

        Args:
            grid (dict): Initial grid of sea cucumbers.
            regions (dict): Number of cucumbers in each region.
            max_x (int): Max x position.
            max_y (int): Max y position.
        """
        self.grid = grid
        self.regions = regions
        self.max_x = max_x
        self.max_y = max_y

    def get_neighbour(self, xy: tuple) -> tuple:
        """Get neighbour of cucumber.

        Args:
            xy (tuple): Cucumber position.

        Returns:
            tuple: Neighbour position.
        """
        region = self.grid[xy]
        x, y = xy
        if region == ">":
            xi = x + 1
            if xi > self.max_x:
                xi = 0
            return (xi, y)
        elif region == "v":
            yi = y + 1
            if yi > self.max_y:
                yi = 0
            return (x, yi)
        return None

    def step(self) -> bool:
        """Perform a step.

        Returns:
            bool: If the cucumbers have remained still or not.
        """
        new_grid = self.grid.copy()
        new_regions = {">": [], "v": [], ".": []}
        still = True
        for herd in [">", "v"]:
            for xy in self.regions[herd]:
                neighbour = self.get_neighbour(xy)
                if neighbour and self.grid[neighbour] == ".":
                    new_regions[herd].append(neighbour)
                    new_grid[neighbour] = self.grid[xy]
                    new_grid[xy] = "."
                    still = False
                else:
                    new_regions[herd].append(xy)
            self.grid.update(new_grid)
        self.regions.update(new_regions)
        return still

    def step_until_still(self) -> int:
        """Determine the number of steps required until cucumbers remain still.

        Returns:
            int: Steps taken.
        """
        still = False
        steps = 0
        while not still:
            steps += 1
            still = self.step()
        return steps


def parse_input(input_file: str) -> Cucumbers:
    """Parse puzzle input.

    Args:
        input_file (str): Puzzle txt file.

    Returns:
        Cucumbers: Cucumbers object.
    """
    o = open(input_file)
    grid = {}
    regions = {">": [], "v": [], ".": []}
    for y, line in enumerate(o.readlines()):
        for x, region in enumerate(line.strip()):
            grid[x, y] = region
            regions[region].append((x, y))
    cucs = Cucumbers(grid, regions, x, y)
    return cucs


# Tests


def test_parse_input():
    cucs = parse_input("day25/example.txt")
    assert type(cucs) == Cucumbers


def test_part_1():
    cucs = parse_input("day25/example.txt")
    assert cucs.step_until_still() == 58


if __name__ == "__main__":
    cucs = parse_input("day25/input.txt")
    answer_1 = cucs.step_until_still()

    print("Day 25 Solutions:")
    print(f"Part 1: {answer_1}")
