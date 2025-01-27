from django.apps import AppConfig

class ChatConfig(AppConfig):
    """
    Configuration class for the 'chat' application.

    This class inherits from django.apps.AppConfig and is used to define
    application-specific configurations such as default auto field and the 
    application's name.
    """

    default_auto_field = 'django.db.models.BigAutoField'  # Specifies the default field type for auto-incrementing primary keys
    name = 'chat'  # The name of the application
