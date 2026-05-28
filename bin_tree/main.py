"""Example entry point for the binary tree assignment variant №9."""

from __future__ import annotations

from pprint import pprint

from binary_tree import gen_bin_tree


def main() -> None:
    """Generate and print a binary tree for assignment variant №9."""

    tree = gen_bin_tree()
    pprint(tree)


if __name__ == "__main__":
    main()
