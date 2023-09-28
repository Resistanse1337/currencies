from datetime import date, timedelta
from decimal import Decimal

import requests
from django.conf import settings


def get_url_by_date(date_: date) -> str:
    return f"https://www.cbr-xml-daily.ru/archive/{date_.strftime('%Y/%m/%d')}/daily_json.js"


def get_rates_data(date_: date) -> dict:
    if date_ == date.today():
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
    else:
        url = get_url_by_date(date_)

    return requests.get(url).json()


def parse_rates_data(data: dict) -> list[tuple[str, Decimal]]:
    result = []

    for info in data["Valute"].values():
        result.append((info["CharCode"], Decimal(round(info["Value"], 2))))

    return result


def get_rates(only_today: bool = True) -> list[tuple[date, list[tuple[str, Decimal]]]]:
    date_ = date.today()
    result = [(date_, parse_rates_data(get_rates_data(date_)))]

    if only_today:
        return result

    i = 0
    while i < settings.COUNT_DAYS_TO_PARSE:
        date_ -= timedelta(days=1)
        data = get_rates_data(date_)

        if data.get("error"):
            continue

        result.append((date_, parse_rates_data(data)))
        i += 1

    return result
