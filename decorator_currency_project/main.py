"""Example of using the currency rates decorators."""

from currency_rates import (
    CbrCurrencyRates,
    CsvCurrencyRatesDecorator,
    YamlCurrencyRatesDecorator,
)


if __name__ == "__main__":
    rates = CbrCurrencyRates()

    json_rates = rates
    yaml_rates = YamlCurrencyRatesDecorator(rates)
    csv_rates = CsvCurrencyRatesDecorator(rates)

    json_rates.save("rates.json")
    yaml_rates.save("rates.yaml")
    csv_rates.save("rates.csv")

    print("Файлы rates.json, rates.yaml и rates.csv успешно созданы.")
