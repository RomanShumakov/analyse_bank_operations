import json
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.api_request import get_currency_rate, get_currency_stocks, settings_reader
from src.utils import cashback_categories, excel_reader, filter_operations, greeting, top_transactions
from src.views import main


@patch("builtins.input", side_effect=["2023", "5"])
@patch("src.views.excel_reader")
@patch("src.views.settings_reader")
@patch("src.views.get_currency_rate")
@patch("src.views.get_currency_stocks")
@patch("src.views.greeting")
def test_main_logic(mock_greet, mock_stocks, mock_rates, mock_settings, mock_excel, mock_input, capsys):
    mock_greet.return_value = "Добрый день"

    # Добавляем все колонки, которые требуют твои функции (Категория, Номер карты/Статус, Описание)
    mock_excel.return_value = pd.DataFrame({
        "Дата операции": ["2023-05-01"],
        "Сумма операции": [100],
        "Категория": ["Еда"],
        "Номер карты": ["*1111"], # Или "Статус", если в коде функций заменил на него
        "Описание": ["Тестовая операция"]
    })

    mock_settings.return_value = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    mock_rates.return_value = [{"currency": "USD", "rate": 80.0}]
    mock_stocks.return_value = [{"stock": "AAPL", "price": 150.0}]

    main()

    # Захватываем весь вывод
    captured = capsys.readouterr()
    full_output = captured.out

    # Находим индекс первой открывающей скобки
    json_start_index = full_output.find('{')

    # Берем всё, что идет от первой скобки и до конца
    json_str = full_output[json_start_index:]

    # Теперь парсим всё целиком
    json_data = json.loads(json_str)

    assert json_data["greeting"] == "Добрый день"
    # ... остальные проверки
