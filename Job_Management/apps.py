from django.apps import AppConfig

class RoomManagementConfig(AppConfig):
    """
    Configuration class for the Room_Management app.
    This class sets up app-specific settings and metadata.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Default field type for auto-generated primary keys
    name = 'Job_Management'  # Name of the app as defined in the project
