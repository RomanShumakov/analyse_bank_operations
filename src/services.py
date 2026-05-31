#Необходимо для сдачи 2 части программы(сервисы - кешбек)
import json

import openpyxl
import pandas as pd

from src.utils import excel_reader, filter_operations


def cashback_categories(df: pd.DataFrame) -> str:
    """Функция возврата суммы всех операций по категориям в json-формате для последующего анализа выгодности кешбека"""
    df = df[df["Сумма операции"] > 0]

    total_df = df[["Категория", "Сумма операции"]].groupby("Категория").sum().reset_index()

    data = total_df.to_dict("records")
    return json.dumps(data, ensure_ascii=False, indent=4)

if __name__ == "__main__":

    while True:
        input_year = input("Введите год: ")
        if 0 < int(input_year) < 9999:
            print(f"Получение данных за {input_year} год")
            break
        else:
            print("Недопустимый ввод")

    while True:
        input_month = input("Введите месяц: ")
        if 1 <= int(input_month) <= 12:
            print(f"Получение данных за {input_month} месяц")
            break
        else:
            print("Недопустимый ввод")

    ex = excel_reader()
    fil = filter_operations(ex, int(input_year), int(input_month))

    operations_summ = cashback_categories(fil)
    print(operations_summ)