from django.apps import AppConfig

class ProductionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'production'

    # Adicione este método ready para carregar os signals
    def ready(self):
        import production.signals