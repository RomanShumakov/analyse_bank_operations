import json
from datetime import datetime

import pandas as pd
from config import PATH_TO_OPERATIONS, PATH_TO_USER_SETTINGS

def excel_reader():
    """Чтение excel-файла с конвертацией в формат DateTime"""
    df = pd.read_excel(PATH_TO_OPERATIONS)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    return df

readed_df = excel_reader()

def filter_operations(operations_df, year, month):
    """Получение данных, отфильтрованных по конкретному месяцу конкретного года"""
    end_date = datetime(year=year, month=month + 1, day=1, ).strftime("%Y-%m-%d %H:%M:%S")
    begin_date = datetime(year=year, month=month, day=1, ).strftime("%Y-%m-%d %H:%M:%S")
    filter_df = operations_df[(operations_df["Дата операции"] >= begin_date) & (operations_df["Дата операции"] < end_date)]
    return filter_df

fill = filter_operations(readed_df, 2021, 4)
fill_dict = fill.to_dict(orient='records')

with open("sas.json", "w", encoding='utf-8') as f:
    json.dump(fill_dict, f, ensure_ascii=False, indent=4)





# from src.greeting import greeting
# from src.services import cashback_categories
#
# def main_func():
#     greet = greeting()
#     card_num = cashback_categories()
#     result = {"greeting": greet, "card": {"last_numbers": card_num, }}