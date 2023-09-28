from datetime import date
from django.test import TestCase
from django.urls import reverse
from django.db.models import Q
from common.tests import CommonAPITestCase
from rates.models import Currency, CurrencyHistory

from rates.parser import get_rates, get_rates_data, get_url_by_date, parse_rates_data
from rates.tasks import parse_rates_task


class RatesAPITestCase(CommonAPITestCase):
    def setUp(self) -> None:
        super().setUp()

        self.currency = Currency.objects.create(charcode="RUB")
        CurrencyHistory.objects.create(currency=self.currency, value=1, date=date(2000, 1, 1))

        parse_rates_task()

    def test_all_rates(self):
        response = self.client.get(reverse("all_rates"))

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(response.json()), 0)

    def test_tracked_rates(self):
        response = self.client.post(
            reverse("user_currency"), 
            data={"currency": self.currency.pk, "threshold": 2}
        )

        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse("tracked_rates")).json()

        self.assertEqual(response[0]["is_threshold_exceeded"], False)

    def test_analytic(self):
        today = date.today()
        response = self.client.get(
            reverse("analytic", kwargs={"pk": Currency.objects.filter(~Q(charcode="RUB")).first().pk}),
            data={"date_from": today, "date_to": today, "threshold": 10}
        )

        self.assertEqual(response.status_code, 200)


class ParserUnitTests(TestCase):
    def test_get_url_by_date(self):
        self.assertEqual(
            get_url_by_date(date(2000, 1, 1)), 
            "https://www.cbr-xml-daily.ru/archive/2000/01/01/daily_json.js"
        )

    def test_get_rates_data(self):
        self.assertNotEqual(
            bool(get_rates_data(date.today())), False
        )

    def test_parse_rates_data(self):
        self.assertNotEqual(
            bool(parse_rates_data(get_rates_data(date.today()))), False
        )

    def test_get_rates(self):
        self.assertNotEqual(
            bool(get_rates(True)), False
        )
