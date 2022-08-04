import ast
from itertools import permutations


def parse_input(input_file: str):
    output = []
    for line in open(input_file).readlines():
        output.append(ast.literal_eval(line))
    return output


class Node:
    def __init__(self, value=None, left=None, right=None, parent=None) -> None:
        """Node class."""
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent

    def add(self, node):
        self.value += node.value


class Tree:
    def __init__(self, number: list) -> None:
        """Tree class.

        Args:
            number (list): List of snailfish.
        """
        self.root = self._make_tree(number)

    @staticmethod
    def _make_tree(number: list, current_node: Node = None) -> Node:
        """Recursively create the initial tree.

        Args:
            number (list): The current snailfish pair to consider.
            current_node (Node, optional): Current node being considered. Defaults to None.

        Returns:
            Node: The root node of the tree.
        """
        if type(number) == list:
            node = Node(parent=current_node)
            node.left = Tree._make_tree(number[0], current_node=node)
            node.right = Tree._make_tree(number[1], current_node=node)
            return node
        elif type(number) == int:
            return Node(value=number, parent=current_node)

    @staticmethod
    def _to_list(node: Node) -> list:
        """Convert the tree to its original list format.

        Args:
            node (Node): Tree.

        Returns:
            list: Origianl list format.
        """
        if type(node.value) == int:
            return node.value
        elif node.value == None:
            return [Tree._to_list(node.left), Tree._to_list(node.right)]

    def __iter__(self):
        return iter(self._to_list(self.root))

    def __add__(self, other):
        """Add two snailfish lists. Perform reduction after added."""
        combined_tree = Tree([list(self), list(other)])
        combined_tree.reduction()
        return combined_tree

    @staticmethod
    def get_explode(node: Node, depth: int = 0) -> Node:
        """Get the node to explode.

        Args:
            node (Node): Node to begin at.
            depth (int, optional): Current depth. Defaults to 0.

        Returns:
            Node: The node to explode.
        """
        if depth == 4:
            return node
        if node.left.value == None:
            left = Tree.get_explode(node.left, depth=depth + 1)
            if type(left) == Node:
                return left
        if node.right.value == None:
            right = Tree.get_explode(node.right, depth=depth + 1)
            if type(right) == Node:
                return right

    @staticmethod
    def get_left(node: Node, previous: Node = None, ascending: bool = True) -> Node:
        """Get the node to the left of current node.

        Args:
            node (Node): Current node.
            previous (Node, optional): Previous node. Defaults to None.
            ascending (bool, optional): If the search is ascending or not. Defaults to True.

        Returns:
            Node: The node to the left of current node.
        """
        if not node:
            return None
        elif type(node.left.value) == int and ascending:
            return node.left
        elif type(node.right.value) == int and not ascending:
            return node.right
        elif node.right.value == None and node.right != previous and not ascending:
            return Tree.get_left(node.right, node, False)
        elif node.left.value == None and node.left != previous and ascending:
            return Tree.get_left(node.left, node, False)
        else:
            return Tree.get_left(node.parent, node)

    @staticmethod
    def get_right(node: Node, previous: Node = None, ascending: bool = True) -> Node:
        """Get the node to the right of current node.

        Args:
            node (Node): Current node.
            previous (Node, optional): Previous node. Defaults to None.
            ascending (bool, optional): If the search is ascending or not. Defaults to True.

        Returns:
            Node: The node to the right of current node.
        """
        if not node:
            return None
        if type(node.right.value) == int and ascending:
            return node.right
        elif type(node.left.value) == int and not ascending:
            return node.left
        elif node.left.value == None and node.left != previous and not ascending:
            return Tree.get_right(node.left, node, False)
        elif node.right.value == None and node.right != previous and ascending:
            return Tree.get_right(node.right, node, False)
        else:
            return Tree.get_right(node.parent, node)

    def explode(self) -> bool:
        """Perform an explosion.

        Returns:
            bool: If an explosion has occured.
        """
        explode_node = self.get_explode(self.root)
        if explode_node:
            left_num = self.get_left(explode_node.parent, explode_node)
            right_num = self.get_right(explode_node.parent, explode_node)
            if left_num:
                left_num.add(explode_node.left)
            if right_num:
                right_num.add(explode_node.right)
            explode_node.value = 0
            explode_node.left = None
            explode_node.right = None
            return True
        else:
            return False

    def split(self) -> bool:
        """Perform a split.

        Returns:
            bool: If a split has occured.
        """
        stack = [self.root]
        while stack:
            n = stack.pop()
            if n.value:
                if n.value >= 10:
                    n.left = Node(value=n.value // 2, parent=n)
                    n.right = Node(value=-(n.value // -2), parent=n)
                    n.value = None
                    return True
            if n.right:
                stack.append(n.right)
            if n.left:
                stack.append(n.left)
        return False

    def reduction(self):
        """Perform reduction. Continue until no more actions can be completed."""
        while True:
            for i in ["explode", "split", None]:
                if not i:
                    return
                change = getattr(self, i)()
                if change:
                    break
                elif not change:
                    continue

    @staticmethod
    def _magnitude(node: Node) -> int:
        """Calculate magnitude of snailfish.

        Args:
            node (Node): Node to begin at.

        Returns:
            int: Magnitude.
        """
        if node.value != None:
            return node.value
        return 3 * Tree._magnitude(node.left) + 2 * Tree._magnitude(node.right)

    @property
    def magnitude(self) -> int:
        """Return magnitude of snailfish.

        Returns:
            int: Magnitude.
        """
        return self._magnitude(self.root)


def add_snailfish(snailfish: list) -> int:
    """Add snailfish together and calculate final magnitude.

    Args:
        snailfish (list): List of snailfish pairs.

    Returns:
        int: Final magnitude.
    """
    tree = Tree(snailfish.pop(0))
    for i in snailfish:
        tree += Tree(i)
    return tree.magnitude


def largest_added_magnitude(snailfish: list) -> int:
    """Find the largest added magnitude.

    Args:
        snailfish (list): List of snailfish pairs.

    Returns:
        int: Largest magnitude of any two different snailfish.
    """
    combos = permutations(snailfish, 2)
    mags = []
    for tree1, tree2 in combos:
        tree = Tree(tree1) + Tree(tree2)
        mags.append(tree.magnitude)
    return max(mags)


# Tests


def test_parse_input():
    output = parse_input("day18/example.txt")
    assert type(output) == list
    assert all(type(i) is list for i in output)


def test_make_tree():
    tree = Tree(([[[[[9, 8], 1], 2], 3], 4]))
    assert list(tree) == [[[[[9, 8], 1], 2], 3], 4]


def test_add():
    tree1 = Tree([[[[4, 3], 4], 4], [7, [[8, 4], 9]]])
    tree2 = Tree([1, 1])
    tree3 = tree1 + tree2
    assert list(tree3) == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]

    tree1 = Tree([[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]])
    tree2 = Tree([7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]])
    tree3 = tree1 + tree2
    assert list(tree3) == [
        [[[4, 0], [5, 4]], [[7, 7], [6, 0]]],
        [[8, [7, 7]], [[7, 9], [5, 0]]],
    ]


def test_explode():
    tree1 = Tree([[[[[9, 8], 1], 2], 3], 4])
    tree2 = Tree([7, [6, [5, [4, [3, 2]]]]])
    tree3 = Tree([[6, [5, [4, [3, 2]]]], 1])
    tree4 = Tree([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]])
    tree5 = Tree([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]])
    tree6 = Tree([[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]])
    tree1.explode()
    tree2.explode()
    tree3.explode()
    tree4.explode()
    tree5.explode()
    tree6.explode()
    assert list(tree1) == [[[[0, 9], 2], 3], 4]
    assert list(tree2) == [7, [6, [5, [7, 0]]]]
    assert list(tree3) == [[6, [5, [7, 0]]], 3]
    assert list(tree4) == [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]
    assert list(tree5) == [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]
    assert list(tree6) == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]


def test_split():
    tree = Tree([[[[0, 7], 4], [15, [0, 13]]], [1, 1]])
    tree.split()
    assert list(tree) == [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]
    tree.split()
    assert list(tree) == [[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]

    tree = Tree([[[[4, 0], [5, 4]], [[7, 0], [15, 5]]], [10, [[11, 9], [11, 0]]]])
    tree.split()
    assert list(tree) == [
        [[[4, 0], [5, 4]], [[7, 0], [[7, 8], 5]]],
        [10, [[11, 9], [11, 0]]],
    ]


def test_magnitude():
    tree = Tree([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]])
    assert tree.magnitude == 3488


def test_part_1():
    output = parse_input("day18/example.txt")
    assert add_snailfish(output) == 4140


def test_part_2():
    output = parse_input("day18/example.txt")
    assert largest_added_magnitude(output) == 3993


if __name__ == "__main__":
    output = parse_input("day18/input.txt")
    answer_1 = add_snailfish(output)
    answer_2 = largest_added_magnitude(output)

    print("Day 18 Solutions:")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")
