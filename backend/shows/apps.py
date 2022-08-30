from django.apps import AppConfig


class ShowsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shows"
    verbose_name = "Show Manager"

    def ready(self):
        import shows.signals.handlers  # noqa
