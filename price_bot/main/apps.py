from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    label = 'main_app'

class PriceBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'price_bot'
    label = 'price_bot_app'
