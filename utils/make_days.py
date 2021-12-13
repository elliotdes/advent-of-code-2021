import os
import shutil


def make_day(day: int):
    """Make a folder that a days challenge.

    Args:
        day (int): Day to make. I.e. 25.
    """
    day_name = f"day{day}"
    if not os.path.exists(day_name):
        os.mkdir(f"{day_name}")
        open(f"{day_name}/input.txt", "a").close()
        open(f"{day_name}/example.txt", "a").close()
        shutil.copy("utils/day_template.py", f"{day_name}")
        os.rename(f"{day_name}/day_template.py", f"{day_name}/{day_name}.py")


if __name__ == "__main__":
    for i in range(1, 26):
        i = "{0:02d}".format(i)
        make_day(i)
