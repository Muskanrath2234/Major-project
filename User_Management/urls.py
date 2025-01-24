"""
This file defines the URL patterns for user profile management in the Django application.

It includes a single route that maps to the 'user_profile' view, which handles the display and 
management of user profiles, ensuring secure access and interaction.

The path defined connects the root URL to the user_profile view.
"""

from django.urls import path  # Importing the path function from Django's URLs module
from .views import user_profile  # Importing the user_profile view from views.py

urlpatterns = [
    path('', user_profile, name='user_profile'),  # Route for the user profile page
]