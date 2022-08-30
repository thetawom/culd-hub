from django.apps import AppConfig


class ShowManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shows"
    verbose_name = "Show Manager"

    def ready(self):
        pass
