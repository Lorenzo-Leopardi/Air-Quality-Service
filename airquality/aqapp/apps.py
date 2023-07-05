from django.apps import AppConfig


class AqAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aqapp'

    def ready(self):
        from . import scheduler
        scheduler.start(5)
