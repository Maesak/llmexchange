import requests
from datetime import datetime
from utils.read_yaml import read_yaml

config = read_yaml("config/model_config.yaml")
FRANKFURTER_BASE_URL = config["FRANKFURTER_BASE_URL"]

def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:

    params = {
        "amount": amount,
        "from": from_currency.upper(),
        "to": to_currency.upper()
    }

    try:
        response = requests.get(FRANKFURTER_BASE_URL, params=params)
        data = response.json()

        rate = data["rates"][to_currency.upper()]
        return {
            "amount": amount,
            "from": from_currency.upper(),
            "to": to_currency.upper(),
            "rate": rate,
            "converted": rate,  
            "ts": datetime.fromisoformat(data["date"])
        }

    except Exception as e:
        raise Exception(f"Currency conversion failed: {e}")

if __name__ == "__main__":
    # Example usage

    result = convert_currency(100, "USD", "EUR")
    print(result)
    # print(f"{result['amount']} {result['from']} = {result['converted']} {result['to']} "
    #         f"(Rate: {result['rate']}, Date: {result['ts'].date()})")
