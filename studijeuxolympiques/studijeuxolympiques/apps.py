from django.apps import AppConfig

class StudijeuxolympiquesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'studijeuxolympiques'

    def ready(self):
        import studijeuxolympiques.signals