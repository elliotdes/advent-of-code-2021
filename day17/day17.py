from collections import defaultdict


def triangular_number(n: int) -> int:
    """Calculate the nth triangle number.

    Args:
        n (int): n.

    Returns:
        int: Triangle number.
    """
    return int(n * (n + 1) / 2)


def part_1(y_min: int) -> int:
    """Calculate part 1.

    Args:
        y_min (int): Minimum y value.

    Returns:
        int: Highest y position.
    """
    v_y = -y_min - 1
    return triangular_number(v_y)


def displacement_x(v_initial: int, time: int) -> int:
    """Calculate displacement in x direction.

    Args:
        v_initial (int): Inital x velocity.
        time (int): Time to travel.

    Returns:
        int: Total displacement in x direction.
    """
    if time > v_initial:
        time = v_initial
    return v_initial * time - triangular_number(time - 1)


def displacement_y(v_initial: int, time: int) -> int:
    """Calculate displacement in y direction.

    Args:
        v_initial (int): Inital y velocity.
        time (int): Time to travel.

    Returns:
        int: Total displacement in y direction.
    """
    return v_initial * time - triangular_number(time - 1)


def valid_initial_velocity(
    velocity: tuple, x_min: int, x_max: int, y_min: int, y_max: int
) -> bool:
    """Check if initial velocity falls within bounds.

    Args:
        velocity (tuple): Initial velocity (x, y).
        x_min (int): Minimum x position.
        x_max (int): Maximum x position.
        y_min (int): Minimum y position.
        y_max (int): Maximum y position.

    Returns:
        bool: If probe falls within bounds during flight.
    """
    v_x, v_y = velocity
    t = 1
    while True:
        d_x = displacement_x(v_x, t)
        d_y = displacement_y(v_y, t)
        if d_x > x_max or d_y < y_min:
            return False
        elif x_min <= d_x <= x_max and y_min <= d_y <= y_max:
            return True
        else:
            t += 1


def part_2(x_min: int, x_max: int, y_min: int, y_max: int) -> int:
    """Solve part 2.

    Args:
        x_min (int): Minimum x position.
        x_max (int): Maximum x position.
        y_min (int): Minimum y position.
        y_max (int): Maximum y position.

    Returns:
        int: Number of distinct velocity values that fall within bounds.
    """
    total = 0
    for v_x in range(1, x_max + 1):
        for v_y in range(y_min, abs(y_min)):
            if valid_initial_velocity((v_x, v_y), x_min, x_max, y_min, y_max):
                total += 1
    return total


# Tests


def test_part_1():
    assert part_1(-10) == 45


def test_displacement_x():
    assert displacement_x(5, 1) == 5
    assert displacement_x(5, 2) == 9
    assert displacement_x(5, 3) == 12
    assert displacement_x(5, 4) == 14
    assert displacement_x(5, 5) == 15
    assert displacement_x(5, 6) == 15
    assert displacement_x(5, 7) == 15
    assert displacement_x(5, 100) == 15


def test_displacement_y():
    assert displacement_y(9, 1) == 9
    assert displacement_y(9, 2) == 17
    assert displacement_y(9, 3) == 24
    assert displacement_y(9, 4) == 30
    assert displacement_y(9, 5) == 35
    assert displacement_y(9, 6) == 39
    assert displacement_y(9, 7) == 42
    assert displacement_y(9, 8) == 44
    assert displacement_y(9, 9) == 45
    assert displacement_y(9, 10) == 45
    assert displacement_y(9, 11) == 44
    assert displacement_y(9, 12) == 42
    assert displacement_y(9, 13) == 39
    assert displacement_y(9, 14) == 35
    assert displacement_y(9, 15) == 30
    assert displacement_y(9, 16) == 24
    assert displacement_y(9, 17) == 17
    assert displacement_y(9, 18) == 9
    assert displacement_y(9, 19) == 0
    assert displacement_y(9, 20) == -10


def test_probe_check():
    assert valid_initial_velocity((1, 2), 20, 30, -10, -5) == False
    assert valid_initial_velocity((7, 2), 20, 30, -10, -5) == True
    assert valid_initial_velocity((6, 3), 20, 30, -10, -5) == True
    assert valid_initial_velocity((9, 0), 20, 30, -10, -5) == True
    assert valid_initial_velocity((17, -4), 20, 30, -10, -5) == False
    assert valid_initial_velocity((6, 9), 20, 30, -10, -5) == True


def test_part_2():
    part_2(20, 30, -10, -5) == 112


if __name__ == "__main__":
    answer_1 = part_1(-126)
    answer_2 = part_2(217, 240, -126, -69)

    print("Day 17 Solutions:")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")
