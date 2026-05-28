"""Tests for the binary_tree module."""

from __future__ import annotations

import unittest
from collections import OrderedDict, defaultdict, deque

from binary_tree import (
    DEFAULT_HEIGHT,
    DEFAULT_ROOT,
    calculate_left_leaf,
    calculate_right_leaf,
    count_nodes,
    gen_bin_tree,
)


class TestBinaryTreeGeneration(unittest.TestCase):
    """Test recursive binary tree generation for variant №9."""

    def test_default_variant_root_children(self) -> None:
        """Default tree should use root 9 and variant №9 formulas."""

        tree = gen_bin_tree(height=2)

        self.assertEqual(tree["value"], DEFAULT_ROOT)
        self.assertEqual(tree["left"]["value"], 19)
        self.assertEqual(tree["right"]["value"], 17)

    def test_default_height_and_root(self) -> None:
        """Default call should use height 6 and root 9."""

        tree = gen_bin_tree()

        self.assertEqual(tree["value"], DEFAULT_ROOT)
        self.assertEqual(count_nodes(tree), 2**DEFAULT_HEIGHT - 1)

    def test_passed_arguments_override_defaults(self) -> None:
        """Passed height and root should be used instead of default values."""

        tree = gen_bin_tree(height=2, root=10)

        self.assertEqual(tree["value"], 10)
        self.assertEqual(tree["left"]["value"], 21)
        self.assertEqual(tree["right"]["value"], 19)

    def test_height_one_contains_only_root(self) -> None:
        """Tree with height 1 should contain only one node."""

        tree = gen_bin_tree(height=1, root=10)

        self.assertEqual(tree, {"value": 10, "left": None, "right": None})
        self.assertEqual(count_nodes(tree), 1)

    def test_node_count_for_height_three(self) -> None:
        """Full binary tree with height 3 should contain 7 nodes."""

        tree = gen_bin_tree(height=3, root=9)

        self.assertEqual(count_nodes(tree), 7)

    def test_leaf_formulas(self) -> None:
        """Left and right child formulas should match variant №9."""

        self.assertEqual(calculate_left_leaf(9), 19)
        self.assertEqual(calculate_right_leaf(9), 17)
        self.assertEqual(calculate_left_leaf(10), 21)
        self.assertEqual(calculate_right_leaf(10), 19)

    def test_invalid_height_raises_value_error(self) -> None:
        """Height less than 1 should be rejected."""

        with self.assertRaises(ValueError):
            gen_bin_tree(height=0)


class TestTreeContainers(unittest.TestCase):
    """Test supported tree containers."""

    def test_list_container(self) -> None:
        """Tree can be generated as a nested list."""

        tree = gen_bin_tree(height=2, container="list")

        self.assertIsInstance(tree, list)
        self.assertEqual(tree[0], 9)
        self.assertEqual(tree[1][0], 19)
        self.assertEqual(tree[2][0], 17)
        self.assertEqual(count_nodes(tree, container="list"), 3)

    def test_ordered_dict_container(self) -> None:
        """Tree can be generated as nested OrderedDict objects."""

        tree = gen_bin_tree(height=1, container="ordered_dict")

        self.assertIsInstance(tree, OrderedDict)
        self.assertEqual(tree["value"], 9)

    def test_defaultdict_container(self) -> None:
        """Tree can be generated as nested defaultdict objects."""

        tree = gen_bin_tree(height=1, container="defaultdict")

        self.assertIsInstance(tree, defaultdict)
        self.assertEqual(tree["value"], 9)
        self.assertIsNone(tree["unknown_key"])

    def test_deque_container(self) -> None:
        """Tree can be generated as nested deque objects."""

        tree = gen_bin_tree(height=2, container="deque")

        self.assertIsInstance(tree, deque)
        self.assertEqual(tree[0], 9)
        self.assertEqual(tree[1][0], 19)
        self.assertEqual(tree[2][0], 17)
        self.assertEqual(count_nodes(tree, container="deque"), 3)

    def test_unsupported_container_raises_value_error(self) -> None:
        """Unknown container name should be rejected."""

        with self.assertRaises(ValueError):
            gen_bin_tree(height=1, container="tuple")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
