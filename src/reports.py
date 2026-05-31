import json
import logging

from config import PATH_TO_LOGGER
from src.views import excel_reader

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(PATH_TO_LOGGER / "services.log", encoding="utf-8", mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def search(data_for_search: str) -> str:
    """Функция поиска в DF по ключевому слову в столбце 'Категория' или 'Описание'"""
    logger.info(f"Начало поиска по запросу: {data_for_search}")

    try:
        df = excel_reader()

        if df is None or df.empty:
            logger.warning("Данные отсутствуют или пустые")
            return json.dumps([], ensure_ascii=False)

        # Поиск по двум колонкам
        filtered_df = df[
            df["Категория"].astype(str).str.contains(data_for_search, case=False)
            | df["Описание"].astype(str).str.contains(data_for_search, case=False)
        ]

        # Добавили date_format='iso', чтобы pytest не ругался
        result_json = filtered_df.to_json(orient="records", force_ascii=False, indent=4, date_format="iso")

        logger.info("Поиск успешно завершен")
        return result_json

    except Exception as e:
        logger.error(f"Ошибка при поиске: {e}")
        return json.dumps([], ensure_ascii=False)
