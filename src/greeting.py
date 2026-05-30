import datetime


def greeting():
    enter_time = datetime.datetime.now().hour
    if 6 <= enter_time < 12:
        return "Доброе утро"
    elif 12 <= enter_time < 18:
        return "Добрый день"
    elif 18 <= enter_time < 24:
        return "Добрый вечер"
    elif 0 <= enter_time < 6:
        return "Доброй ночи"

