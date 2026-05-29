"""Classes for getting and converting currency rates.

The module contains a simple implementation of the Decorator pattern.
The base component returns currency rates in JSON format. Decorators
wrap the base component and convert the same data to YAML or CSV.
"""

from __future__ import annotations

import csv
import json
from abc import ABC, abstractmethod
from io import StringIO
from pathlib import Path
from typing import Any
from urllib.request import urlopen

import yaml

DEFAULT_CBR_URL = "https://www.cbr-xml-daily.ru/daily_json.js"


class CurrencyRatesComponent(ABC):
    """Define a common interface for components and decorators."""

    @abstractmethod
    def get_data(self) -> dict[str, Any]:
        """Return currency rates as a dictionary."""

    @abstractmethod
    def operation(self) -> str:
        """Return currency rates in the selected text format."""

    @abstractmethod
    def save(self, file_path: str | Path) -> Path:
        """Save formatted currency rates to a file and return its path."""


class CbrCurrencyRates(CurrencyRatesComponent):
    """Get currency rates and return them in JSON format.

    Parameters
    ----------
    url:
        Address of the service with currency rates in JSON format.
    data:
        Optional ready-made data. It is useful for tests and examples,
        because it allows the class to work without an Internet connection.
    """

    def __init__(
        self,
        url: str = DEFAULT_CBR_URL,
        data: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the component with an API URL or prepared data."""
        self.url = url
        self._data = data

    def get_data(self) -> dict[str, Any]:
        """Return rates from prepared data or load them from the API."""
        if self._data is None:
            with urlopen(self.url, timeout=10) as response:
                self._data = json.loads(response.read().decode("utf-8"))
        return self._data

    def operation(self) -> str:
        """Return currency rates in JSON format."""
        return json.dumps(self.get_data(), ensure_ascii=False, indent=2)

    def save(self, file_path: str | Path) -> Path:
        """Save currency rates to a JSON file."""
        path = Path(file_path)
        path.write_text(self.operation(), encoding="utf-8")
        return path


class CurrencyRatesDecorator(CurrencyRatesComponent):
    """Base decorator that stores a wrapped component."""

    def __init__(self, component: CurrencyRatesComponent) -> None:
        """Initialize the decorator with another component."""
        self._component = component

    def get_data(self) -> dict[str, Any]:
        """Return data from the wrapped component."""
        return self._component.get_data()

    def operation(self) -> str:
        """Return data in the format of the wrapped component."""
        return self._component.operation()

    def save(self, file_path: str | Path) -> Path:
        """Save data using the wrapped component."""
        return self._component.save(file_path)


class YamlCurrencyRatesDecorator(CurrencyRatesDecorator):
    """Decorator that converts currency rates to YAML format."""

    def operation(self) -> str:
        """Return currency rates in YAML format."""
        return yaml.safe_dump(
            self.get_data(),
            allow_unicode=True,
            sort_keys=False,
        )

    def save(self, file_path: str | Path) -> Path:
        """Save currency rates to a YAML file."""
        path = Path(file_path)
        path.write_text(self.operation(), encoding="utf-8")
        return path


class CsvCurrencyRatesDecorator(CurrencyRatesDecorator):
    """Decorator that converts currency rates to CSV format."""

    def operation(self) -> str:
        """Return currency rates in CSV format."""
        output = StringIO()
        fieldnames = ["CharCode", "Name", "Nominal", "Value"]
        writer = csv.DictWriter(output, fieldnames=fieldnames)

        writer.writeheader()
        for currency in self.get_data()["Valute"].values():
            writer.writerow(
                {
                    "CharCode": currency["CharCode"],
                    "Name": currency["Name"],
                    "Nominal": currency["Nominal"],
                    "Value": currency["Value"],
                }
            )

        return output.getvalue()

    def save(self, file_path: str | Path) -> Path:
        """Save currency rates to a CSV file."""
        path = Path(file_path)
        path.write_text(self.operation(), encoding="utf-8", newline="")
        return path
