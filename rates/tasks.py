from django.core.cache import cache

from currencies.celery import app
from rates.models import Currency, CurrencyHistory
from rates.parser import get_rates


@app.task
def parse_rates_task():
    cache.clear()

    only_today = True
    if not CurrencyHistory.objects.first():
        only_today = False

    all_rates = get_rates(only_today)

    currency_objects = []
    currency_history_objects = []

    currencies = {c.charcode: c for c in Currency.objects.all()}

    for date_, rate_batch in all_rates:
        for rate in rate_batch:
            char_code, value = rate

            currency = currencies.get(char_code)
            if not currency:
                currency = Currency(charcode=char_code)
                currencies[char_code] = currency
                currency_objects.append(currency)
    
    Currency.objects.bulk_create(currency_objects, ignore_conflicts=True)

    currencies = {c.charcode: c for c in Currency.objects.all()}

    for date_, rate_batch in all_rates:
        if CurrencyHistory.objects.filter(date=date_).exists():
            continue

        for rate in rate_batch:
            char_code, value = rate

            currency = currencies[char_code]
            currency_history_objects.append(
                CurrencyHistory(
                    currency=currency,
                    value=value,
                    date=date_
                )
            )

    CurrencyHistory.objects.bulk_create(currency_history_objects)
    
