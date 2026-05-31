import json
from datetime import datetime

def greeting():
    enter_time = datetime.now().hour
    if 6 <= enter_time < 12:
        return "Доброе утро"
    elif 12 <= enter_time < 18:
        return "Добрый день"
    elif 18 <= enter_time < 24:
        return "Добрый вечер"
    elif 0 <= enter_time < 6:
        return "Доброй ночи"

import pandas as pd
from config import PATH_TO_OPERATIONS, PATH_TO_USER_SETTINGS
import openpyxl

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
fill["Дата операции"] = fill["Дата операции"].astype(str)
fill_dict = fill.to_dict(orient='records')

with open("sas.json", "w", encoding='utf-8') as f:
    json.dump(fill_dict, f, ensure_ascii=False, indent=4)


def cashback_categories() -> list[dict]:
    """Функция возврата суммы всех трат по каждой карте и получения кешбека"""
    df = pd.read_excel(PATH_TO_OPERATIONS)
    df = df[df["Сумма операции"] < 0]
    df["last_digits"] = df["Номер карты"].str.replace('*', '')
    df["total_spent"] = df["Сумма операции"].abs()
    df["cashback"] = round(df["total_spent"] / 100, 2)

    total_df = df[["last_digits", "total_spent", "cashback"]].groupby("last_digits").sum().reset_index()

    data = total_df.to_dict("records")
    return data
