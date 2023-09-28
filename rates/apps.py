from django.apps import AppConfig


class RatesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rates'

    def ready(self) -> None:
        import rates.signals  # noqa
        return super().ready()
