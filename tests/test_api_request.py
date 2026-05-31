import unittest
from unittest.mock import patch, mock_open
import json

# Предположим, твой файл называется utils.py, замени на реальное имя
from src.api_request import settings_reader, get_currency_rate, get_currency_stocks

class TestFinancialUtils(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='{"user": "settings"}')
    @patch("json.load")
    def test_settings_reader(self, mock_json_load, mock_file):
        """Тестируем чтение настроек"""
        mock_json_load.return_value = {"user": "settings"}
        result = settings_reader()
        self.assertEqual(result, {"user": "settings"})
        mock_file.assert_called_once()

    @patch("requests.get")
    def test_get_currency_rate(self, mock_get):
        """Тестируем получение курса валют (Mock ЦБ РФ)"""
        # Имитируем ответ от API ЦБ
        mock_response = mock_get.return_value
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 90.5},
                "EUR": {"Value": 100.2}
            }
        }

        codes = ["USD"]
        # Превращаем генератор в список, чтобы проверить данные
        result = list(get_currency_rate(codes))

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["currency_code"], "USD")
        self.assertEqual(result[0]["rate"], 90.5)

    @patch("requests.get")
    def test_get_currency_stocks(self, mock_get):
        """Тестируем получение акций (Mock MOEX)"""
        # Имитируем ответ от MOEX
        mock_response = mock_get.return_value
        mock_response.json.return_value = {
            "securities": {
                "data": [
                    [None, None, None, 250.5] # Цена сидит в 4-м элементе (индекс 3)
                ]
            }
        }

        stocks = ["GAZP"]
        result = list(get_currency_stocks(stocks))

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["stock"], "GAZP")
        self.assertEqual(result[0]["price"], 250.5)

if __name__ == "__main__":
    unittest.main()
