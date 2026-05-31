import json

from src.api_request import get_currency_rate, get_currency_stocks, settings_reader
from src.utils import cashback_categories, excel_reader, filter_operations, greeting, top_transactions


def main():
    """Основная логика программы, вынесенная в функцию"""
    while True:
        input_year = input("Введите год: ")
        if input_year.isdigit() and 0 < int(input_year) < 9999:
            print(f"Получение данных за {input_year} год")
            break
        else:
            print("Недопустимый ввод")

    while True:
        input_month = input("Введите месяц: ")
        if input_month.isdigit() and 1 <= int(input_month) <= 12:
            print(f"Получение данных за {input_month} месяц")
            break
        else:
            print("Недопустимый ввод")

    greet = greeting()
    excel_to_df = excel_reader()
    filtered_df = filter_operations(excel_to_df, int(input_year), int(input_month))

    cards = cashback_categories(filtered_df)
    top_5 = top_transactions(filtered_df)

    settings_dict = settings_reader()
    code = settings_dict["user_currencies"]
    stock = settings_dict["user_stocks"]

    currency_rates = list(get_currency_rate(code))
    stock_prices = list(get_currency_stocks(stock))

    resulto = {
        "greeting": greet,
        "cards": cards,
        "top_transactions": top_5,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    print(json.dumps(resulto, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    main()
