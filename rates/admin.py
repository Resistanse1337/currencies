from django.contrib import admin

from rates.models import Currency, CurrencyHistory, TrackedQuote


@admin.register(CurrencyHistory)
class CurrencyHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "currency", "value", "date", "created_at",)
    list_display_links = ("id",)
    ordering = ("pk", )


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "charcode",)
    list_display_links = ("id",)
    ordering = ("pk", )


@admin.register(TrackedQuote)
class TrackedQuoteAdmin(admin.ModelAdmin):
    list_display = ("id", "currency", "threshold",)
    list_display_links = ("id",)
    ordering = ("pk", )
