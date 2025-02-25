from django.apps import AppConfig


class AgricolaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Agro'

    def ready(self):
        import Agro.signals  
