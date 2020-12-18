from django.apps import AppConfig
from django.conf import settings

class UniBotConfig(AppConfig):
    name = 'bot'

    def ready(self):
        pass