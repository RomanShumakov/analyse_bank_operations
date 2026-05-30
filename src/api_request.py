import requests
import json


def get_currency_rate(code):
    jsonfile = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    datafile = jsonfile.json()
    for valute_code in datafile["Valute"]:
        if valute_code == code:
            return {
                "currency_code": code,
                "rate": datafile["Valute"][code]["Value"]
            }

# wanted = "EUR"
# result = get_currency_rate(wanted)
# print(json.dumps(result, indent=4))

rate = get_currency_rate("USD")
print(rate)

api_2 = "https://api.frankfurter.dev/v2/rates?base=USD&quotes=RUB"