from django.apps import AppConfig


class AdministratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.api.administrator'

    def ready(self):
        import apps.api.administrator.signals
