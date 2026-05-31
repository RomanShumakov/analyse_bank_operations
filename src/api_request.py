import requests
import json
from config import PATH_TO_USER_SETTINGS
from typing import Generator, Dict


def settings_reader() -> dict[list]:
    """Расшифровка пользовательских конфигураций"""
    with open(PATH_TO_USER_SETTINGS, "r", encoding='utf-8') as file:
        return json.load(file)

settings_dict = settings_reader()
coder = settings_dict["user_currencies"]
stocker = settings_dict["user_stocks"]


def get_currency_rate(codes: list) -> Generator[dict]:
    """Функция получения настроенных пользователем курсов валют от ЦБ РФ"""
    jsonfile = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    datafile = jsonfile.json()
    for valute_code in datafile["Valute"]:
        if valute_code in codes:
            yield {
                "currency_code": valute_code,
                "rate": datafile["Valute"][valute_code]["Value"]
            }


def get_currency_stocks(stocks: list) -> Generator[dict]:
    """Функция получения цен настроенных пользователем акций по интернет-запросу к сайту iss.moex.com"""
    for stock in stocks:
        jsonfile = requests.get(f"https://iss.moex.com/iss/engines/stock/markets/shares/securities/{stock}.json")
        datafile = jsonfile.json()
        yield {"stock": stock, "price": datafile["securities"]["data"][0][3]}
