import json
from datetime import datetime
import pandas as pd
from config import PATH_TO_OPERATIONS, PATH_TO_USER_SETTINGS
import openpyxl

def greeting() -> str:
    "Функция приветствия пользователя в зависсимости от времени использования программы"
    enter_time = datetime.now().hour
    if 6 <= enter_time < 12:
        return "Доброе утро"
    elif 12 <= enter_time < 18:
        return "Добрый день"
    elif 18 <= enter_time < 24:
        return "Добрый вечер"
    elif 0 <= enter_time < 6:
        return "Доброй ночи"


def excel_reader():
    """Чтение excel-файла с конвертацией в формат DateTime"""
    df = pd.read_excel(PATH_TO_OPERATIONS)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    return df


def filter_operations(operations_df: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
    """Получение данных, отфильтрованных по конкретному месяцу конкретного года"""
    end_date = datetime(year=year, month=month + 1, day=1, ).strftime("%Y-%m-%d %H:%M:%S")
    begin_date = datetime(year=year, month=month, day=1, ).strftime("%Y-%m-%d %H:%M:%S")
    filter_df = operations_df[(operations_df["Дата операции"] >= begin_date) & (operations_df["Дата операции"] < end_date)]
    return filter_df


def cashback_categories(df: pd.DataFrame) -> list[dict]:
    """Функция возврата суммы всех трат по каждой карте и получения кешбека"""
    df = df[df["Сумма операции"] < 0]
    df["last_digits"] = df["Номер карты"].str.replace('*', '')
    df["total_spent"] = df["Сумма операции"].abs()
    df["cashback"] = round(df["total_spent"] / 100, 2)

    total_df = df[["last_digits", "total_spent", "cashback"]].groupby("last_digits").sum().reset_index()

    data = total_df.to_dict("records")
    return data

def top_transactions(df: pd.DataFrame) -> list[dict]:
    """Функция возврата суммы всех трат по каждой карте и получения кешбека"""
    df = df[df["Сумма операции"] < 0]

    df = df.rename(columns={
        "Дата операции": "date",
        "Сумма операции": "amount",
        "Категория": "category",
        "Описание": "description"
    })

    # Преобразование формата даты, если необходимо
    df["date"] = pd.to_datetime(df["date"]).dt.strftime('%d.%m.%Y')
    df["amount"] = df["amount"].abs()

    # Сортировка по сумме и выбор топ-5
    top_5_df = df.sort_values(by="amount", ascending=False).head(5)

    # Преобразование в формат JSON
    data = top_5_df[["date", "amount", "category", "description"]].to_dict("records")
    return data


