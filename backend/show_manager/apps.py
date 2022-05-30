from django.apps import AppConfig


class ShowManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "show_manager"
    verbose_name = "Show Manager"

    def ready(self):
        import show_manager.signals.handlers  # noqa
