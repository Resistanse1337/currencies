from django.core.cache import cache
from django.db.models.signals import pre_save
from django.dispatch import receiver

from rates.models import Currency, CurrencyHistory


@receiver(pre_save, sender=Currency)
@receiver(pre_save, sender=CurrencyHistory)
def my_callback(sender, instance, *args, **kwargs):
    cache.clear()
