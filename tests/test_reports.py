import json
from unittest.mock import patch, Mock

import pandas as pd

from src.reports import search


@patch("src.reports.excel_reader")
def test_search_success(mock_excel: Mock) -> None:
    mock_excel.return_value = pd.DataFrame(
        [
            {"Категория": "Продукты", "Описание": "Пятерочка", "Сумма": -500},
            {"Категория": "Кофе", "Описание": "Старбакс", "Сумма": -300},
        ]
    )
    result = search("кофе")
    data = json.loads(result)
    assert len(data) == 1
    assert data[0]["Категория"] == "Кофе"


@patch("src.reports.excel_reader")
def test_search_no_results(mock_excel: Mock) -> None:
    mock_excel.return_value = pd.DataFrame([{"Категория": "Продукты", "Описание": "Молоко", "Сумма": -100}])
    result = search("Авиабилеты")
    data = json.loads(result)
    assert data == []


@patch("src.reports.excel_reader")
def test_search_empty_df(mock_excel: Mock) -> None:
    mock_excel.return_value = pd.DataFrame()
    result = search("Что угодно")
    assert json.loads(result) == []


@patch("src.reports.excel_reader")
def test_search_exception(mock_excel: Mock) -> None:
    mock_excel.side_effect = Exception("Crash!")
    result = search("test")
    assert json.loads(result) == []
