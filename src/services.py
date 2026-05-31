#Необходимо для сдачи 2 части программы(сервисы - кешбек)
import json
import pandas as pd
from config import PATH_TO_OPERATIONS
import json
import openpyxl

def cashback_categories():
    """Функция возврата суммы всех операций по категориям в json-формате для последующего анализа выгодности кешбека"""
    df = pd.read_excel(PATH_TO_OPERATIONS)
    df = df[df["Сумма операции"] > 0]

    total_df = df[["Категория", "Сумма операции"]].groupby("Категория").sum().reset_index()

    data = total_df.to_dict("records")
    return json.dumps(data, ensure_ascii=False, indent=4)

a = cashback_categories()
print(a)