from django.apps import AppConfig

class FinanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finance'

    def ready(import_self):
        import finance.signals # <-- Importa os signals quando o app iniciar