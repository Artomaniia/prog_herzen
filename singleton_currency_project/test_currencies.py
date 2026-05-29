"""Tests for the singleton currency service."""

from __future__ import annotations

import os
import tempfile
import unittest
from unittest.mock import Mock, patch

from currencies import CurrenciesRates


SAMPLE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<ValCurs Date="01.01.2026" name="Foreign Currency Market">
    <Valute ID="R01035">
        <NumCode>826</NumCode>
        <CharCode>GBP</CharCode>
        <Nominal>1</Nominal>
        <Name>Фунт стерлингов Соединенного королевства</Name>
        <Value>113,2069</Value>
    </Valute>
    <Valute ID="R01335">
        <NumCode>398</NumCode>
        <CharCode>KZT</CharCode>
        <Nominal>100</Nominal>
        <Name>Казахстанских тенге</Name>
        <Value>19,8264</Value>
    </Valute>
    <Valute ID="R01700J">
        <NumCode>949</NumCode>
        <CharCode>TRY</CharCode>
        <Nominal>10</Nominal>
        <Name>Турецких лир</Name>
        <Value>33,1224</Value>
    </Valute>
</ValCurs>
"""


class FakeResponse:
    """Small fake HTTP response for tests."""

    content = SAMPLE_XML.encode("utf-8")

    def raise_for_status(self) -> None:
        """Simulate a successful HTTP response."""
        return None


class TestCurrenciesRates(unittest.TestCase):
    """Test cases for CurrenciesRates."""

    def setUp(self) -> None:
        """Reset singleton state before each test."""
        CurrenciesRates.reset_instance()

    def test_singleton_returns_same_object(self) -> None:
        """Two constructor calls must return the same object."""
        first = CurrenciesRates(["R01035"], request_interval=0)
        second = CurrenciesRates(["R01335"], request_interval=0)
        self.assertIs(first, second)
        self.assertEqual(second.currencies_ids, ["R01335"])

    @patch("currencies.requests.get", return_value=FakeResponse())
    def test_invalid_currency_id_returns_none(self, mock_get: Mock) -> None:
        """Wrong CBR identifier must be returned with None value."""
        service = CurrenciesRates(["R9999"], request_interval=0)
        self.assertEqual(service.get_currencies(), [{"R9999": None}])
        mock_get.assert_called_once()

    @patch("currencies.requests.get", return_value=FakeResponse())
    def test_correct_gbp_name(self, mock_get: Mock) -> None:
        """GBP must have the expected Russian currency name."""
        service = CurrenciesRates(["R01035"], request_interval=0)
        result = service.get_currencies()
        self.assertEqual(
            result[0]["GBP"][0],
            "Фунт стерлингов Соединенного королевства",
        )
        mock_get.assert_called_once()

    @patch("currencies.requests.get", return_value=FakeResponse())
    def test_correct_value_is_in_expected_range(self, mock_get: Mock) -> None:
        """A valid currency rate must be in the range from 0 to 999."""
        service = CurrenciesRates(["R01700J"], request_interval=0)
        result = service.get_currencies()
        rate_parts = result[0]["TRY"][1]
        rate = float(f"{rate_parts[0]}.{rate_parts[1]}")
        self.assertGreater(rate, 0)
        self.assertLess(rate, 999)
        mock_get.assert_called_once()

    @patch("currencies.requests.get", return_value=FakeResponse())
    def test_rate_is_stored_as_two_parts(self, mock_get: Mock) -> None:
        """Currency rate must be stored as integer and fractional parts."""
        service = CurrenciesRates(["R01035"], request_interval=0)
        result = service.get_currencies()
        self.assertEqual(result[0]["GBP"][1], ("113", "2069"))
        mock_get.assert_called_once()

    @patch("currencies.requests.get", return_value=FakeResponse())
    def test_nominal_is_saved_when_not_equal_to_one(self, mock_get: Mock) -> None:
        """Currency nominal must be saved when it is not equal to 1."""
        service = CurrenciesRates(["R01335"], request_interval=0)
        result = service.get_currencies()
        self.assertEqual(result[0]["KZT"][2], 100)
        mock_get.assert_called_once()

    @patch("currencies.requests.get", return_value=FakeResponse())
    def test_getters_and_setters(self, mock_get: Mock) -> None:
        """Properties must allow controlled reading and updating of data."""
        service = CurrenciesRates(request_interval=0)
        service.currencies_ids = ["R01035"]
        self.assertEqual(service.currencies_ids, ["R01035"])
        service.request_interval = 0.5
        self.assertEqual(service.request_interval, 0.5)
        service.source_url = "https://example.com/rates.xml"
        self.assertEqual(service.source_url, "https://example.com/rates.xml")
        service.get_currencies()
        mock_get.assert_called_once()

    @patch("currencies.requests.get", return_value=FakeResponse())
    def test_visualization_creates_file(self, mock_get: Mock) -> None:
        """Visualization method must save a chart image."""
        service = CurrenciesRates(["R01035", "R01335", "R01700J"], request_interval=0)
        service.get_currencies()

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "currencies.jpg")
            result_path = service.visualize_currencies(filename)
            self.assertTrue(os.path.exists(result_path))
            self.assertGreater(os.path.getsize(result_path), 0)

        mock_get.assert_called_once()


if __name__ == "__main__":
    unittest.main()
