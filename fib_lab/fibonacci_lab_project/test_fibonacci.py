"""Tests for the Fibonacci laboratory work."""

import unittest

from fibonacci import (
    FibonacchiLst,
    FibonacchiLstGetItem,
    FibonacciGetItem,
    FibonacciIterator,
    fibonacci_numbers,
    is_fibonacci_number,
    my_genn,
)


class TestFibonacciNumbers(unittest.TestCase):
    """Tests for the helper function that creates Fibonacci lists."""

    def test_zero_count(self) -> None:
        """Function should return an empty list for zero elements."""
        self.assertEqual(fibonacci_numbers(0), [])

    def test_one_count(self) -> None:
        """Function should return only zero for one element."""
        self.assertEqual(fibonacci_numbers(1), [0])

    def test_eight_numbers(self) -> None:
        """Function should return the first eight Fibonacci numbers."""
        self.assertEqual(fibonacci_numbers(8), [0, 1, 1, 2, 3, 5, 8, 13])

    def test_negative_count_error(self) -> None:
        """Function should not accept negative counts."""
        with self.assertRaises(ValueError):
            fibonacci_numbers(-1)

    def test_float_count_error(self) -> None:
        """Function should not accept a non-integer count."""
        with self.assertRaises(TypeError):
            fibonacci_numbers(2.5)  # type: ignore[arg-type]


class TestFibonacciIterators(unittest.TestCase):
    """Tests for simplified and regular Fibonacci iterators."""

    def test_getitem_iterator(self) -> None:
        """Simplified iterator should work through Python iteration protocol."""
        result = list(FibonacciGetItem(6))
        self.assertEqual(result, [0, 1, 1, 2, 3, 5])

    def test_regular_iterator(self) -> None:
        """Regular iterator should return the same Fibonacci sequence."""
        result = list(FibonacciIterator(6))
        self.assertEqual(result, [0, 1, 1, 2, 3, 5])

    def test_iterators_are_equal(self) -> None:
        """Both iterator implementations should produce equal results."""
        self.assertEqual(list(FibonacciGetItem(10)), list(FibonacciIterator(10)))

    def test_iterator_stop_iteration(self) -> None:
        """Regular iterator should raise StopIteration after the last item."""
        iterator = FibonacciIterator(1)
        self.assertEqual(next(iterator), 0)
        with self.assertRaises(StopIteration):
            next(iterator)


class TestFibonacchiLst(unittest.TestCase):
    """Tests for filtering Fibonacci numbers from a list."""

    def test_normal_list(self) -> None:
        """Iterator should return Fibonacci numbers from a normal list."""
        result = list(FibonacchiLst([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1]))
        self.assertEqual(result, [0, 1, 2, 3, 5, 8, 1])

    def test_empty_list(self) -> None:
        """Iterator should return an empty list for an empty source."""
        self.assertEqual(list(FibonacchiLst([])), [])

    def test_duplicates(self) -> None:
        """Iterator should keep duplicate Fibonacci numbers from the source."""
        self.assertEqual(list(FibonacchiLst([1, 1])), [1, 1])

    def test_getitem_filtering(self) -> None:
        """Simplified filtering iterator should return the same values."""
        result = list(FibonacchiLstGetItem(range(10)))
        self.assertEqual(result, [0, 1, 2, 3, 5, 8])

    def test_negative_number_is_not_fibonacci(self) -> None:
        """Negative values should not be treated as Fibonacci numbers."""
        self.assertFalse(is_fibonacci_number(-1))


class TestFibonacciCoroutine(unittest.TestCase):
    """Tests for the Fibonacci coroutine."""

    def test_three_numbers(self) -> None:
        """Coroutine should return three first Fibonacci numbers."""
        gen = my_genn()
        self.assertEqual(gen.send(3), [0, 1, 1])

    def test_five_numbers(self) -> None:
        """Coroutine should return five first Fibonacci numbers."""
        gen = my_genn()
        self.assertEqual(gen.send(5), [0, 1, 1, 2, 3])

    def test_multiple_send_calls(self) -> None:
        """Coroutine should correctly handle several send calls."""
        gen = my_genn()
        self.assertEqual(gen.send(3), [0, 1, 1])
        self.assertEqual(gen.send(8), [0, 1, 1, 2, 3, 5, 8, 13])

    def test_invalid_count(self) -> None:
        """Coroutine should pass validation errors from fibonacci_numbers."""
        gen = my_genn()
        with self.assertRaises(ValueError):
            gen.send(-5)


if __name__ == "__main__":
    unittest.main()
