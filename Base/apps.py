# Importing the required module from Django
from django.apps import AppConfig

# BaseConfig class for the 'base' app configuration
class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Specifies the default auto-incrementing field type for primary keys (BigAutoField)
    name = 'Base'  # The name of the app, in this case, 'base'
