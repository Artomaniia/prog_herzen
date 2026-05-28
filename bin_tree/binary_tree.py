"""Utilities for generating a binary tree for assignment variant №9.

The module contains a recursive implementation of :func:`gen_bin_tree`.
The default assignment parameters are fixed according to variant №9:
``root = 9``, ``height = 6``, ``left = root * 2 + 1`` and
``right = 2 * root - 1``.

The base representation of the tree is a nested dictionary. Additionally,
the tree can be stored in a ``list`` or in containers from :mod:`collections`:
``OrderedDict``, ``defaultdict`` and ``deque``.
"""

from __future__ import annotations

from collections import OrderedDict, defaultdict, deque
from typing import Any, DefaultDict, Deque, Literal, TypeAlias

Number: TypeAlias = int | float
TreeDict: TypeAlias = dict[str, Any]
TreeList: TypeAlias = list[Any]
TreeOrderedDict: TypeAlias = OrderedDict[str, Any]
TreeDefaultDict: TypeAlias = DefaultDict[str, Any]
TreeDeque: TypeAlias = Deque[Any]
Tree: TypeAlias = TreeDict | TreeList | TreeOrderedDict | TreeDefaultDict | TreeDeque | None
ContainerName: TypeAlias = Literal["dict", "list", "ordered_dict", "defaultdict", "deque"]

DEFAULT_ROOT: int = 9
DEFAULT_HEIGHT: int = 6


def calculate_left_leaf(root: Number) -> Number:
    """Calculate the left child value according to variant №9.

    Args:
        root: Value stored in the current node.

    Returns:
        Value for the left child node.
    """

    return root * 2 + 1


def calculate_right_leaf(root: Number) -> Number:
    """Calculate the right child value according to variant №9.

    Args:
        root: Value stored in the current node.

    Returns:
        Value for the right child node.
    """

    return 2 * root - 1


def gen_bin_tree(
    height: int | None = None,
    root: Number | None = None,
    *,
    container: ContainerName = "dict",
) -> Tree:
    """Generate a binary tree recursively.

    The function builds a binary tree where each node has no more than two
    children. Child values are calculated by the formulas from assignment
    variant №9:

    - left child: ``root * 2 + 1``;
    - right child: ``2 * root - 1``.

    If ``height`` or ``root`` is not passed, the function uses the default
    values from variant №9: ``height = 6`` and ``root = 9``.

    Args:
        height: Height of the tree. ``1`` means that only the root node is
            created. If omitted, the default height for variant №9 is used.
        root: Value stored in the current root node. If omitted, the default
            root for variant №9 is used.
        container: Container used for storing tree nodes. Supported values are
            ``"dict"``, ``"list"``, ``"ordered_dict"``, ``"defaultdict"`` and
            ``"deque"``.

    Returns:
        A binary tree in the selected container format.

    Raises:
        ValueError: If ``height`` is less than ``1``.
        ValueError: If an unsupported container name is passed.
    """

    actual_height = DEFAULT_HEIGHT if height is None else height
    actual_root = DEFAULT_ROOT if root is None else root

    if actual_height < 1:
        raise ValueError("height must be greater than or equal to 1")

    return _build_tree(height=actual_height, root=actual_root, container=container)


def _build_tree(height: int, root: Number, container: ContainerName) -> Tree:
    """Recursively build a binary tree node.

    Args:
        height: Height of the current subtree.
        root: Value stored in the current node.
        container: Container used for storing the current node.

    Returns:
        A subtree in the selected container format.
    """

    if height == 1:
        return _make_node(root, None, None, container)

    left_value = calculate_left_leaf(root)
    right_value = calculate_right_leaf(root)

    left_node = _build_tree(height - 1, left_value, container)
    right_node = _build_tree(height - 1, right_value, container)

    return _make_node(root, left_node, right_node, container)


def _make_node(root: Number, left: Tree, right: Tree, container: ContainerName) -> Tree:
    """Create a tree node in the selected container format.

    Args:
        root: Value stored in the node.
        left: Left child node.
        right: Right child node.
        container: Container used for node creation.

    Returns:
        A tree node represented by the chosen container.

    Raises:
        ValueError: If the container name is unsupported.
    """

    if container == "dict":
        return {"value": root, "left": left, "right": right}

    if container == "list":
        return [root, left, right]

    if container == "ordered_dict":
        return OrderedDict((("value", root), ("left", left), ("right", right)))

    if container == "defaultdict":
        node: TreeDefaultDict = defaultdict(lambda: None)
        node["value"] = root
        node["left"] = left
        node["right"] = right
        return node

    if container == "deque":
        return deque((root, left, right))

    raise ValueError(f"Unsupported container: {container}")


def count_nodes(tree: Tree, *, container: ContainerName = "dict") -> int:
    """Count nodes in a generated binary tree.

    Args:
        tree: Tree returned by :func:`gen_bin_tree`.
        container: Container format used by the tree.

    Returns:
        Number of nodes in the tree.
    """

    if tree is None:
        return 0

    left, right = _get_children(tree, container)
    return 1 + count_nodes(left, container=container) + count_nodes(right, container=container)


def _get_children(tree: Tree, container: ContainerName) -> tuple[Tree, Tree]:
    """Return left and right children for a tree node.

    Args:
        tree: Current tree node.
        container: Container format used by the tree.

    Returns:
        A tuple containing the left and right child nodes.

    Raises:
        ValueError: If the container name is unsupported.
    """

    if tree is None:
        return None, None

    if container in {"dict", "ordered_dict", "defaultdict"}:
        return tree["left"], tree["right"]  # type: ignore[index]

    if container in {"list", "deque"}:
        return tree[1], tree[2]  # type: ignore[index]

    raise ValueError(f"Unsupported container: {container}")


if __name__ == "__main__":
    print(gen_bin_tree())
