from django.apps import AppConfig

# Configuration class for the User_Post application
class UserPostConfig(AppConfig):
    # Specifies the type of auto-generated field to be used for model IDs
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Name of the application
    name = 'Post'