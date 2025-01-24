from django.contrib import admin  # Import Django's admin module for managing the admin interface
from .models import UserProfile  # Import the UserProfile model for registration in the admin site

admin.site.register(UserProfile)  # Register the UserProfile model with the admin site
