from src.utils import greeting, excel_reader, filter_operations, cashback_categories, top_transactions
from src.api_request import settings_reader, get_currency_rate, get_currency_stocks
import json



greet = greeting()
excel_to_df = excel_reader()
filtered_df = filter_operations(excel_to_df, 2021, 3)

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
    "stock_prices": stock_prices
}


print(json.dumps(resulto, ensure_ascii=False, indent=4))