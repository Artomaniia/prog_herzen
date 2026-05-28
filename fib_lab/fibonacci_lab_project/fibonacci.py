"""Utilities for working with Fibonacci numbers.

The module contains three parts required by the laboratory task:

* a simplified iterator based only on ``__getitem__``;
* a regular iterator based on ``__iter__`` and ``__next__``;
* a coroutine that returns a list of Fibonacci numbers for a received length.
"""

from __future__ import annotations

import functools
from collections.abc import Callable, Generator, Iterable, Iterator
from typing import TypeVar

T = TypeVar("T", bound=Callable[..., Generator[list[int] | None, int, None]])


def fibonacci_numbers(count: int) -> list[int]:
    """Return the first ``count`` Fibonacci numbers.

    Args:
        count: Number of Fibonacci elements to generate.

    Returns:
        A list containing the first ``count`` Fibonacci numbers.

    Raises:
        ValueError: If ``count`` is negative.
        TypeError: If ``count`` is not an integer.
    """
    if not isinstance(count, int):
        raise TypeError("count must be an integer")
    if count < 0:
        raise ValueError("count must be non-negative")

    numbers: list[int] = []
    first, second = 0, 1

    for _ in range(count):
        numbers.append(first)
        first, second = second, first + second

    return numbers


def is_fibonacci_number(value: int) -> bool:
    """Check whether ``value`` belongs to the Fibonacci sequence.

    Args:
        value: Integer value to check.

    Returns:
        ``True`` if the value is a Fibonacci number, otherwise ``False``.
    """
    if not isinstance(value, int):
        return False
    if value < 0:
        return False

    first, second = 0, 1
    while first < value:
        first, second = second, first + second

    return first == value


class FibonacciGetItem:
    """Simplified Fibonacci iterator implemented with ``__getitem__`` only.

    Python can iterate over an object that implements ``__getitem__`` and raises
    ``IndexError`` when the sequence is over. This class uses that simplified
    protocol and returns the first ``count`` Fibonacci numbers.
    """

    def __init__(self, count: int) -> None:
        """Create a simplified iterator for the first ``count`` numbers."""
        if not isinstance(count, int):
            raise TypeError("count must be an integer")
        if count < 0:
            raise ValueError("count must be non-negative")

        self.count = count
        self._numbers = fibonacci_numbers(count)

    def __getitem__(self, index: int) -> int:
        """Return a Fibonacci number by index.

        Args:
            index: Position of an element in the generated sequence.

        Returns:
            Fibonacci number at the selected position.

        Raises:
            IndexError: If the index is outside the generated sequence.
        """
        if index < 0 or index >= self.count:
            raise IndexError("FibonacciGetItem index out of range")
        return self._numbers[index]


class FibonacciIterator(Iterator[int]):
    """Regular Fibonacci iterator using ``__iter__`` and ``__next__``."""

    def __init__(self, count: int) -> None:
        """Create an iterator for the first ``count`` Fibonacci numbers."""
        if not isinstance(count, int):
            raise TypeError("count must be an integer")
        if count < 0:
            raise ValueError("count must be non-negative")

        self.count = count
        self._index = 0
        self._current = 0
        self._next_value = 1

    def __iter__(self) -> FibonacciIterator:
        """Return the iterator object itself."""
        return self

    def __next__(self) -> int:
        """Return the next Fibonacci number.

        Raises:
            StopIteration: If all requested numbers have already been returned.
        """
        if self._index >= self.count:
            raise StopIteration

        result = self._current
        self._current, self._next_value = (
            self._next_value,
            self._current + self._next_value,
        )
        self._index += 1
        return result


class FibonacchiLst(Iterator[int]):
    """Iterator that returns Fibonacci numbers from a given iterable.

    The class name keeps the spelling from the original task. It scans the
    provided iterable and yields only those elements that belong to the
    Fibonacci sequence.
    """

    def __init__(self, instance: Iterable[int]) -> None:
        """Create an iterator over Fibonacci numbers from ``instance``."""
        self.instance = list(instance)
        self.idx = 0

    def __iter__(self) -> FibonacchiLst:
        """Return the iterator object itself."""
        return self

    def __next__(self) -> int:
        """Return the next Fibonacci number found in the source iterable."""
        while self.idx < len(self.instance):
            result = self.instance[self.idx]
            self.idx += 1

            if is_fibonacci_number(result):
                return result

        raise StopIteration


class FibonacchiLstGetItem:
    """Simplified version of ``FibonacchiLst`` based on ``__getitem__``."""

    def __init__(self, instance: Iterable[int]) -> None:
        """Save only Fibonacci numbers from ``instance`` for indexed access."""
        self._numbers = [number for number in instance if is_fibonacci_number(number)]

    def __getitem__(self, index: int) -> int:
        """Return a Fibonacci number from the filtered list by index."""
        if index < 0 or index >= len(self._numbers):
            raise IndexError("FibonacchiLstGetItem index out of range")
        return self._numbers[index]


def fib_coroutine(function: T) -> T:
    """Prime a Fibonacci coroutine before first use.

    Args:
        function: Coroutine function that expects the first ``send`` value only
            after being primed.

    Returns:
        A wrapper that creates and primes the coroutine.
    """

    @functools.wraps(function)
    def inner(*args: object, **kwargs: object) -> Generator[list[int] | None, int, None]:
        generator = function(*args, **kwargs)
        generator.send(None)
        return generator

    return inner  # type: ignore[return-value]


@fib_coroutine
def my_genn() -> Generator[list[int] | None, int, None]:
    """Return a coroutine that generates Fibonacci lists.

    The coroutine receives an integer ``n`` through ``send`` and returns a list
    containing the first ``n`` Fibonacci numbers.

    Examples:
        >>> gen = my_genn()
        >>> gen.send(3)
        [0, 1, 1]
        >>> gen.send(5)
        [0, 1, 1, 2, 3]
    """
    count = yield
    while True:
        count = yield fibonacci_numbers(count)
