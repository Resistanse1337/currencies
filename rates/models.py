from datetime import date
from decimal import Decimal
from django.conf import settings

from django.core.cache import cache
from django.db.models import Max, F, Case, When, Value, Min, OuterRef, Subquery
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.manager import BaseManager

from common.models import LifetimeModel
from users.models import User


class Currency(models.Model):
    class Meta:
        verbose_name = _("Валюта")
        verbose_name_plural = _("Валюты")
    
    charcode = models.CharField(max_length=8, verbose_name=_("Буквенный код"), unique=True)

    @property
    def current_rate(self) -> Decimal:
        return CurrencyHistory.objects.get(currency=self, date=CurrencyHistory.max_date()).value

    def __str__(self) -> str:
        return self.charcode


class CurrencyHistory(LifetimeModel):
    class Meta:
        verbose_name = _("Курс валюты")
        verbose_name_plural = _("Курс валют")

        unique_together = ("currency", "date")

    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name=_("Валюта"))
    value = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Значение в рублях"))
    date = models.DateField(verbose_name=_("Дата обновления курса"))

    @staticmethod
    def max_date() -> "date":
        return CurrencyHistory.objects.aggregate(max_date=Max("date"))["max_date"]
    
    @staticmethod
    def last_rates() -> BaseManager["CurrencyHistory"]:
        if last_rates := cache.get(settings.ALL_RATES_CACHE):
            return last_rates

        last_rates = CurrencyHistory.objects.select_related("currency").filter(date=CurrencyHistory.max_date())
        cache.set(settings.ALL_RATES_CACHE, last_rates, settings.ALL_RATES_CACHE_TIMEOUT)

        return last_rates
    
    @staticmethod
    def min_value(date_from: "date | str", date_to: "date | str", currency_id: int) -> Decimal:
        return CurrencyHistory.objects.filter(
            date__range=[date_from, date_to], currency__id=currency_id
        ).aggregate(min_value=Min("value"))["min_value"]
    
    @staticmethod
    def max_value(date_from: "date | str", date_to: "date | str", currency_id: int) -> Decimal:
        return CurrencyHistory.objects.filter(
            date__range=[date_from, date_to], currency__id=currency_id
        ).aggregate(max_value=Max("value"))["max_value"]
    
    @staticmethod
    def get_analytic(
        date_from: "date | str", date_to: "date | str", currency_id: int, threshold: Decimal
    ) -> BaseManager["CurrencyHistory"]:
        return CurrencyHistory.objects.select_related("currency").filter(
            date__range=[date_from, date_to], currency__id=currency_id
        ).annotate(
            is_threshold_exceeded=Case(
                When(value__gte=threshold, then=True),
                default=False,
            )
        ).annotate(
            threshold_match_type=Case(
                When(value__gt=threshold, then=Value("more")),
                When(value__lt=threshold, then=Value("less")),
                When(value=threshold, then=Value("equal")),
            )
        ).annotate(
            is_min_value=Case(
                When(value=CurrencyHistory.min_value(date_from, date_to, currency_id), then=True),
                default=False
            )
        ).annotate(
            is_max_value=Case(
                When(value=CurrencyHistory.max_value(date_from, date_to, currency_id), then=True),
                default=False
            )
        ).annotate(
            percentage_ratio=F("value") / Decimal(threshold) * Decimal(100)
        )

    def __str__(self) -> str:
        return f"{self.currency.charcode} {self.value}"


class TrackedQuote(LifetimeModel):
    class Meta:
        verbose_name = _("Отслеживаемая валюта")
        verbose_name_plural = _("Отслеживаемые котировки")

        unique_together = ("user", "currency")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, verbose_name=_("Котируемая валюта")
    )
    threshold = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Пороговое значение"))

    @staticmethod
    def tracked_quotes_for_user(user: User) -> BaseManager["TrackedQuote"]:
        currency_history = CurrencyHistory.objects.filter(
            currency=OuterRef("currency__pk"), date=CurrencyHistory.max_date()
        )

        return TrackedQuote.objects.select_related(
            "currency"
        ).filter(
            user=user
        ).annotate(
            value=Subquery(currency_history.values("value"))
        ).annotate(
            is_threshold_exceeded=Case(
                When(threshold__lt=F("value"), then=True),
                default=False
            )
        )

    def __str__(self) -> str:
        return f"{self.user} {self.currency} {self.threshold}"
