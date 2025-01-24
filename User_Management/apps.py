from django.apps import AppConfig  # Import Django's AppConfig class for application configuration

# Configuration for the User Management application
class UserManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Specify the default auto-increment field type
    name = 'User_Management'  # Name of the application
