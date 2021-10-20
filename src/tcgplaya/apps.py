from django.apps import AppConfig


class TcgplayaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tcgplaya'

    # connect receivers for user profile to be added after a user account is created
    def ready(self):
        import tcgplaya.models