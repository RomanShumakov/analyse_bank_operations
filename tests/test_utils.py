from freezegun import freeze_time

import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import patch

from src.utils import greeting, filter_operations, cashback_categories, top_transactions


def test_greeting():
    """Функция теста приветствия"""
    with freeze_time("2025-01-23 00:00:00"):
        greet = greeting()
        assert greet == "Доброй ночи"

    with freeze_time("2025-01-23 08:00:00"):
        greet = greeting()
        assert greet == "Доброе утро"

    with freeze_time("2025-01-23 12:00:00"):
        greet = greeting()
        assert greet == "Добрый день"

    with freeze_time("2025-01-23 18:00:00"):
        greet = greeting()
        assert greet == "Добрый вечер"

def test_filter_operations():
    """Функция теста фильтрации"""
    data = {
        "Дата операции": ["2023-05-01", "2023-05-15", "2023-06-01"]
    }
    df = pd.DataFrame(data)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"])

    # Фильтруем май (5 месяц) 2023 года
    result = filter_operations(df, 2023, 5)
    assert len(result) == 2

def test_cashback_categories():
    """Функция тестирования кешбэка по картам"""
    data = {
        "Номер карты": ["*1234", "*1234", "*5678"],
        "Сумма операции": [-1000.0, -2000.0, -500.0]
    }
    df = pd.DataFrame(data)
    result = cashback_categories(df)

    # Проверяем карту *1234 (должно быть 1000 + 2000 = 3000 трат и 30 кешбэка)
    card_1234 = next(item for item in result if item["last_digits"] == "1234")
    assert card_1234["total_spent"] == 3000.0
    assert card_1234["cashback"] == 30.0


def test_top_transactions():
    """Функция тестирования топ-5 транзакций"""
    data = {
        "Дата операции": ["01.01.2023"] * 6,
        "Сумма операции": [-100, -500, -200, -1000, -50, -300],
        "Категория": ["А"] * 6,
        "Описание": ["Б"] * 6
    }
    df = pd.DataFrame(data)
    result = top_transactions(df)

    assert len(result) == 5
    # Самая крупная трата (1000) должна быть первой
    assert result[0]["amount"] == 1000.0



