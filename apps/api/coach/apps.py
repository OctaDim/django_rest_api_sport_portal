from django.apps import AppConfig


class CoachConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.api.coach'

    def ready(self):
        import apps.api.coach.signals
