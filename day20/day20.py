from collections import defaultdict

pixel_map = {"#": 1, ".": 0}


class Enhancement:
    def __init__(self, algorithm: str, image_list: list):
        """Trench map.

        Args:
            algorithm (str): Image enhancement algorithm.
            image_list (list): Input image.
        """
        self.algorithm = algorithm

        self.min_x = 0
        self.min_y = 0
        self.max_x = len(image_list[0])
        self.max_y = len(image_list)

        self.input_image = {}
        for y in range(len(image_list)):
            for x in range(len(image_list[0])):
                self.input_image[x, y] = pixel_map[image_list[y][x]]

        self.increase_margins()

    @property
    def lit_pixels(self) -> int:
        """Return number of lit pixels.

        Returns:
            int: Lit pixels.
        """
        return sum(self.input_image.values())

    def increase_margins(self, margin=2):
        """Increase margins.

        Args:
            margin (int, optional): Value to increase margin by. Defaults to 2.
        """
        self.min_x -= margin
        self.min_y -= margin
        self.max_x += margin
        self.max_y += margin

    def step(self, steps: int):
        """Perform a step.

        Args:
            steps (int): Number of steps to take.
        """
        for i in range(steps):
            to_update = {}
            for y in range(self.min_y, self.max_y + 1):
                for x in range(self.min_x, self.max_x + 1):
                    output_pixel = self.calc_pixel(x, y, i)
                    # Update at the end
                    to_update[x, y] = output_pixel

            for x, y in to_update:
                self.input_image[x, y] = to_update[x, y]
            self.increase_margins()

    def calc_pixel(self, x: int, y: int, step: int) -> int:
        """Determine pixel value.

        Args:
            x (int): x position.
            y (int): y position.
            step (int): Current step.

        Returns:
            int: Pixel value.
        """
        bin_num = ""
        for dx, dy in [
            (-1, -1),
            (0, -1),
            (1, -1),
            (-1, 0),
            (0, 0),
            (1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
        ]:
            infinite_pixel = step % (pixel_map[self.algorithm[0]] + 1)
            pixel = self.input_image.get((x + dx, y + dy), infinite_pixel)
            bin_num += str(pixel)
        output_pixel = pixel_map[self.algorithm[int(bin_num, 2)]]
        return output_pixel


def parse_input(input_file: str) -> Enhancement:
    """Parse puzzle input.

    Args:
        input_file (str): Input txt file.

    Returns:
        Enhancement: Trench map puzzle output.
    """
    o = open(input_file)
    o = o.read()
    algorithm, image_str = o.split("\n\n")
    image_list = image_str.split("\n")

    enhance = Enhancement(algorithm, image_list)
    return enhance


def print_grid(grid: dict) -> str:
    """Print coordinates inside a 2D matrix.
    Used for debugging.

    Args:
        grid (dict): Coordinates.

    Returns:
        str: Printable string representation of matrix.
    """
    max_x = max(x for x, _ in grid) + 1
    max_y = max(y for _, y in grid) + 1
    matrix = [["." for _ in range(max_x)] for _ in range(max_y)]
    for x, y in grid:
        if grid[x, y]:
            matrix[y][x] = "#"
    printable_matrix = "\n".join(["".join(i) for i in matrix])
    return "\n" + printable_matrix


# Tests


def test_parse_input():
    enhance = parse_input("day20/example.txt")
    assert type(enhance) == Enhancement


def test_part_enhance():
    enhance = parse_input("day20/example.txt")
    assert enhance.lit_pixels == 10
    enhance.step(2)
    assert enhance.lit_pixels == 35
    enhance.step(48)
    assert enhance.lit_pixels == 3351


if __name__ == "__main__":
    enhance = parse_input("day20/input.txt")
    print("Day 20 Solutions:")
    enhance.step(2)
    print(f"Part 1: {enhance.lit_pixels}")
    enhance.step(48)
    print(f"Part 2: {enhance.lit_pixels}")
