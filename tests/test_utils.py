# import json
# from unittest.mock import patch
# import pytest
from freezegun import freeze_time
# from pandas import DataFrame, Timestamp
#
# from config import PATH_TO_OPERATIONS, PATH_TO_USER_SETTINGS
from src.utils import greeting


def test_greeting():
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


