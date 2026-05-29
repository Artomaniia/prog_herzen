"""Tests for currency rates components and decorators."""

import csv
import json
import tempfile
import unittest
from io import StringIO
from pathlib import Path

import yaml

from currency_rates import (
    CbrCurrencyRates,
    CsvCurrencyRatesDecorator,
    YamlCurrencyRatesDecorator,
)


TEST_DATA = {
    "Date": "2026-01-01T11:30:00+03:00",
    "Valute": {
        "USD": {
            "CharCode": "USD",
            "Name": "Доллар США",
            "Nominal": 1,
            "Value": 90.0,
        },
        "EUR": {
            "CharCode": "EUR",
            "Name": "Евро",
            "Nominal": 1,
            "Value": 100.0,
        },
    },
}


class TestCbrCurrencyRates(unittest.TestCase):
    """Test the base JSON component."""

    def setUp(self) -> None:
        """Create a component with prepared data before each test."""
        self.component = CbrCurrencyRates(data=TEST_DATA)

    def test_operation_returns_json(self) -> None:
        """The base component should return a valid JSON string."""
        result = self.component.operation()
        data = json.loads(result)

        self.assertEqual(data["Valute"]["USD"]["Value"], 90.0)
        self.assertIn("EUR", data["Valute"])

    def test_save_creates_json_file(self) -> None:
        """The base component should save data to a JSON file."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rates.json"
            self.component.save(path)
            saved_data = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(saved_data["Valute"]["EUR"]["Name"], "Евро")


class TestYamlCurrencyRatesDecorator(unittest.TestCase):
    """Test the YAML decorator."""

    def setUp(self) -> None:
        """Create a YAML decorator with prepared data before each test."""
        component = CbrCurrencyRates(data=TEST_DATA)
        self.decorator = YamlCurrencyRatesDecorator(component)

    def test_operation_returns_yaml(self) -> None:
        """The YAML decorator should return a valid YAML string."""
        result = self.decorator.operation()
        data = yaml.safe_load(result)

        self.assertEqual(data["Valute"]["USD"]["CharCode"], "USD")
        self.assertEqual(data["Valute"]["EUR"]["Value"], 100.0)

    def test_save_creates_yaml_file(self) -> None:
        """The YAML decorator should save data to a YAML file."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rates.yaml"
            self.decorator.save(path)
            saved_data = yaml.safe_load(path.read_text(encoding="utf-8"))

        self.assertIn("USD", saved_data["Valute"])


class TestCsvCurrencyRatesDecorator(unittest.TestCase):
    """Test the CSV decorator."""

    def setUp(self) -> None:
        """Create a CSV decorator with prepared data before each test."""
        component = CbrCurrencyRates(data=TEST_DATA)
        self.decorator = CsvCurrencyRatesDecorator(component)

    def test_operation_returns_csv(self) -> None:
        """The CSV decorator should return a valid CSV string."""
        result = self.decorator.operation()
        rows = list(csv.DictReader(StringIO(result)))

        self.assertEqual(rows[0]["CharCode"], "USD")
        self.assertEqual(rows[1]["Name"], "Евро")

    def test_save_creates_csv_file(self) -> None:
        """The CSV decorator should save data to a CSV file."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rates.csv"
            self.decorator.save(path)
            rows = list(csv.DictReader(StringIO(path.read_text(encoding="utf-8"))))

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["Value"], "90.0")


if __name__ == "__main__":
    unittest.main()
