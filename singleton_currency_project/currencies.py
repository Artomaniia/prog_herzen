"""Tools for loading currency rates from the Central Bank of Russia.

The module demonstrates the Singleton design pattern implemented through a
metaclass. The main class can request currencies by their CBR identifiers,
store rate values as separate integer and fractional parts, and save a simple
bar chart with selected currency rates.
"""

from __future__ import annotations

import time
from typing import Any, TypeAlias
from xml.etree import ElementTree as ET

import requests


RateParts: TypeAlias = tuple[str, str]
CurrencyInfo: TypeAlias = tuple[str, RateParts] | tuple[str, RateParts, int]
CurrencyResult: TypeAlias = dict[str, CurrencyInfo | None]


class SingletonMeta(type):
    """Metaclass that allows only one instance of a class to exist."""

    _instances: dict[type, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Return an existing instance or create the first one."""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        else:
            instance = cls._instances[cls]
            if hasattr(instance, "configure"):
                instance.configure(*args, **kwargs)
        return cls._instances[cls]


class CurrenciesRates(metaclass=SingletonMeta):
    """Load and store selected currency rates from the CBR XML service.

    Parameters
    ----------
    currencies_ids:
        List of currency identifiers from the CBR service, for example
        ``["R01035", "R01335", "R01700J"]``.
    request_interval:
        Minimum delay in seconds between two real HTTP requests.
    source_url:
        URL of the XML service with daily currency rates.
    """

    DEFAULT_URL = "https://www.cbr.ru/scripts/XML_daily.asp"

    def __init__(
        self,
        currencies_ids: list[str] | None = None,
        request_interval: float = 1.0,
        source_url: str = DEFAULT_URL,
    ) -> None:
        """Initialize the currency service and input parameters."""
        self._currencies_ids: list[str] = currencies_ids or [
            "R01035",
            "R01335",
            "R01700J",
        ]
        self._request_interval = float(request_interval)
        self._source_url = source_url
        self._result: list[CurrencyResult] = []
        self._last_request_time = 0.0

    def __del__(self) -> None:
        """Clear stored attributes before object destruction."""
        self._currencies_ids = []
        self._result = []
        self._last_request_time = 0.0

    @classmethod
    def reset_instance(cls) -> None:
        """Remove the singleton instance.

        This helper is useful for tests, because each test can start with a
        clean object state.
        """
        SingletonMeta._instances.pop(cls, None)

    def configure(
        self,
        currencies_ids: list[str] | None = None,
        request_interval: float | None = None,
        source_url: str | None = None,
    ) -> None:
        """Update input parameters of the existing singleton object."""
        if currencies_ids is not None:
            self.currencies_ids = currencies_ids
        if request_interval is not None:
            self.request_interval = request_interval
        if source_url is not None:
            self.source_url = source_url

    @property
    def currencies_ids(self) -> list[str]:
        """Return the list of selected CBR currency identifiers."""
        return self._currencies_ids

    @currencies_ids.setter
    def currencies_ids(self, value: list[str]) -> None:
        """Set the list of selected CBR currency identifiers."""
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise TypeError("currencies_ids must be a list of strings")
        self._currencies_ids = value

    @currencies_ids.deleter
    def currencies_ids(self) -> None:
        """Delete the list of selected CBR currency identifiers."""
        self._currencies_ids = []

    @property
    def request_interval(self) -> float:
        """Return the minimum delay between real HTTP requests."""
        return self._request_interval

    @request_interval.setter
    def request_interval(self, value: float) -> None:
        """Set the minimum delay between real HTTP requests."""
        if value < 0:
            raise ValueError("request_interval cannot be negative")
        self._request_interval = float(value)

    @request_interval.deleter
    def request_interval(self) -> None:
        """Reset the request interval to the default value."""
        self._request_interval = 1.0

    @property
    def source_url(self) -> str:
        """Return the URL of the CBR XML service."""
        return self._source_url

    @source_url.setter
    def source_url(self, value: str) -> None:
        """Set the URL of the CBR XML service."""
        if not value:
            raise ValueError("source_url cannot be empty")
        self._source_url = value

    @source_url.deleter
    def source_url(self) -> None:
        """Reset the XML service URL to the default one."""
        self._source_url = self.DEFAULT_URL

    @property
    def result(self) -> list[CurrencyResult]:
        """Return the last loaded currency result."""
        return self._result

    @result.setter
    def result(self, value: list[CurrencyResult]) -> None:
        """Set the last loaded currency result."""
        self._result = value

    @result.deleter
    def result(self) -> None:
        """Delete the stored currency result."""
        self._result = []

    @staticmethod
    def _split_rate(value: str) -> RateParts:
        """Split a currency rate into integer and fractional parts."""
        normalized_value = value.replace(".", ",")
        integer_part, fractional_part = normalized_value.split(",", maxsplit=1)
        return integer_part, fractional_part

    def _wait_before_request(self) -> None:
        """Pause execution if the previous request was too recent."""
        passed_time = time.monotonic() - self._last_request_time
        wait_time = self._request_interval - passed_time
        if wait_time > 0:
            time.sleep(wait_time)

    def _load_xml_root(self) -> ET.Element:
        """Send an HTTP request and return the parsed XML root element."""
        self._wait_before_request()
        response = requests.get(self._source_url, timeout=10)
        response.raise_for_status()
        self._last_request_time = time.monotonic()
        return ET.fromstring(response.content)

    @staticmethod
    def _make_currency_item(valute: ET.Element) -> CurrencyResult:
        """Convert one XML currency element to the required result format."""
        char_code = valute.findtext("CharCode", default="")
        name = valute.findtext("Name", default="")
        nominal = int(valute.findtext("Nominal", default="1"))
        value = valute.findtext("Value", default="0,0")
        rate_parts = CurrenciesRates._split_rate(value)

        if nominal == 1:
            return {char_code: (name, rate_parts)}
        return {char_code: (name, rate_parts, nominal)}

    def get_currencies(self, currencies_ids: list[str] | None = None) -> list[CurrencyResult]:
        """Return selected currencies in the required format.

        If a requested identifier is absent in the XML document, the method
        returns a dictionary with this identifier and ``None`` as value.
        """
        if currencies_ids is not None:
            self.currencies_ids = currencies_ids

        root = self._load_xml_root()
        valutes_by_id = {valute.get("ID"): valute for valute in root.findall("Valute")}

        result: list[CurrencyResult] = []
        for currency_id in self._currencies_ids:
            valute = valutes_by_id.get(currency_id)
            if valute is None:
                result.append({currency_id: None})
            else:
                result.append(self._make_currency_item(valute))

        self._result = result
        return result

    @staticmethod
    def _rate_to_float(currency_info: CurrencyInfo) -> float:
        """Convert stored integer and fractional parts to a float value."""
        rate_parts = currency_info[1]
        return float(f"{rate_parts[0]}.{rate_parts[1]}")

    def visualize_currencies(self, filename: str = "currencies.jpg") -> str:
        """Save a bar chart with selected currency rates to an image file.

        Parameters
        ----------
        filename:
            Name of the image file for the saved chart.

        Returns
        -------
        str
            Path to the saved chart image.
        """
        if not self._result:
            self.get_currencies()

        import matplotlib.pyplot as plt

        codes: list[str] = []
        values: list[float] = []

        for item in self._result:
            code, currency_info = next(iter(item.items()))
            if currency_info is None:
                continue
            codes.append(code)
            values.append(self._rate_to_float(currency_info))

        if not codes:
            raise ValueError("There are no valid currencies to visualize")

        fig, ax = plt.subplots()
        ax.bar(codes, values)
        ax.set_title("Курсы валют")
        ax.set_xlabel("Валюта")
        ax.set_ylabel("Курс, руб.")
        fig.tight_layout()
        fig.savefig(filename, format="jpg")
        plt.close(fig)
        return filename
