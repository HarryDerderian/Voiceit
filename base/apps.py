from django.apps import AppConfig

# This file is required to connect base logic to main django logic... don't delete
class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'
