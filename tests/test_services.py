import pytest
import pandas as pd
import json
# Замени 'your_filename' на имя файла, который ты мне скинул
from src.services import cashback_categories

def test_cashback_categories_positive():
    """Проверяем, что сумма считается только для положительных операций и группируется"""
    data = {
        "Категория": ["Супермаркеты", "Супермаркеты", "Аптеки", "Зарплата"],
        "Сумма операции": [100.50, 200.00, 50.00, -500.00] # -500 должно отсеяться
    }
    df = pd.DataFrame(data)

    result_json = cashback_categories(df)
    result = json.loads(result_json)

    # Должно остаться 2 категории: Супермаркеты (300.5) и Аптеки (50.0)
    assert len(result) == 2

    # Ищем конкретную категорию в списке словарей
    supermarket = next(item for item in result if item["Категория"] == "Супермаркеты")
    assert supermarket["Сумма операции"] == 300.50

def test_cashback_empty_df():
    """Проверяем работу с пустым DataFrame"""
    df = pd.DataFrame(columns=["Категория", "Сумма операции"])
    result_json = cashback_categories(df)
    assert result_json == "[]"
