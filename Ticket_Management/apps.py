from django.apps import AppConfig

"""
This file defines the configuration for the Ticket Management app in a Django project.
It sets the default model field type and the name of the app.
"""

class TicketManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Specifies the default field type for auto-incrementing fields
    name = 'Ticket_Management'  # Name of the application
