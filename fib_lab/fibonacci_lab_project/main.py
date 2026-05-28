"""Example script for the Fibonacci laboratory work."""

from fibonacci import FibonacchiLst, FibonacciGetItem, FibonacciIterator, my_genn


def main() -> None:
    """Show examples of all implemented Fibonacci tools."""
    print("Simplified iterator with __getitem__:")
    print(list(FibonacciGetItem(8)))

    print("Regular iterator with __iter__ and __next__:")
    print(list(FibonacciIterator(8)))

    print("Filtering Fibonacci numbers from a list:")
    print(list(FibonacchiLst([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1])))

    print("Coroutine result:")
    gen = my_genn()
    print(gen.send(8))


if __name__ == "__main__":
    main()
