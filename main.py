import api
import requests

from requests import Response


API_KEY = api.EXCHANGE_API


class CurrencyConverter:
    """A class to handle currency conversion using the ExchangeRate-API."""

    def __init__(self, ex_api: str, convert_from: str, convert_into: str, amount_to_convert: int) -> None:
        """
        Initialize the CurrencyConverter class with the given parameters.

        Args:
            ex_api (str): API key for the exchange rate API.
            convert_from (str): Currency code to convert from.
            convert_into (str): Currency code to convert into.
            amount_to_convert (int): Amount of currency to convert.
        """
        self.ex_api = ex_api
        self.convert_from = convert_from
        self.convert_into = convert_into
        self.amount_to_convert = amount_to_convert
        self.exchange_data: Response | None = None

    def exchange_response(self) -> Response:
        """
        Make a request to the exchange rate API and get the exchange data.

        Returns:
            Response: The response from the exchange rate API.
        """
        self.exchange_data = requests.get(f"https://v6.exchangerate-api.com/v6/{self.ex_api}"
                                          f"/pair/{self.convert_from}/{self.convert_into}/{self.amount_to_convert}")

        return self.exchange_data

    def response(self) -> str:
        """
        Process the exchange data and return the result as a string.

        Returns:
            str: A string with the conversion rate and the result of the currency conversion.
        """
        result = self.exchange_response()

        if result.status_code == 200:
            # If the request is successful, extract the conversion rate and result from the JSON response

            return (f"Conversion rate for pair "
                    f"{self.convert_from}/{self.convert_into}: {result.json()["conversion_rate"]} "
                    f"\nFor exchanging {self.amount_to_convert} {self.convert_from} "
                    f"you will get {result.json()["conversion_result"]} {self.convert_into}")
        else:
            # If the request fails, return an error message with the status code
            return f"Request error. Status code: {result.status_code}"


def main():
    """
    Main function to run the currency converter.
    """
    currency_from = input("Enter currency to convert from."
                          "\nUse ISO 4217 Three Letter Currency Codes - e.g. USD for US Dollars, EUR for Euro etc."
                          "\n>>>  ")

    currency_into = input("Enter currency to convert to."
                          "\nUse ISO 4217 Three Letter Currency Codes - e.g. USD for US Dollars, EUR for Euro etc."
                          "\n>>>  ")

    amount = int(input("Enter the amount to convert: "))

    # Create an instance of the CurrencyConverter with the input data
    first_exchange = CurrencyConverter(API_KEY, currency_from, currency_into, amount)

    print(first_exchange.response())


if __name__ == "__main__":
    main()
