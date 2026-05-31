import requests
import json
from config import PATH_TO_USER_SETTINGS


def settings_reader() -> list:
    """Расшифровка пользовательских конфигураций с извлечением валютных кодов"""
    with open(PATH_TO_USER_SETTINGS, "r", encoding='utf-8') as file:
        settings_dict = json.load(file)
        return settings_dict["user_currencies"]

# res = settings_reader()
# print(res)


def get_currency_rate(codes: list) -> dict:
    """Получение настроенных пользователем курсов валют от ЦБ РФ"""
    jsonfile = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    datafile = jsonfile.json()
    for valute_code in datafile["Valute"]:
        if valute_code in codes:
            yield {
                "currency_code": valute_code,
                "rate": datafile["Valute"][valute_code]["Value"]
            }

# codes = ["USD", "EUR"]
# rate = get_currency_rate(codes)
# print(list(rate))

api_2 = "https://api.frankfurter.dev/v2/rates?base=USD&quotes=RUB"