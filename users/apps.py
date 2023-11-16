from django.apps import AppConfig

# Lets our main django project know about this dir and its logic.
class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
