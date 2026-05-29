"""Example of using the singleton currency service."""

from currencies import CurrenciesRates


if __name__ == "__main__":
    service = CurrenciesRates(["R01035", "R01335", "R01700J"])
    currencies = service.get_currencies()
    print(currencies)
    service.visualize_currencies("currencies.jpg")
    print("График сохранен в файл currencies.jpg")
