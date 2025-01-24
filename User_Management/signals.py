"""
This file handles the signals for creating and saving user profiles 
when a User instance is created or updated.

It ensures that:
- UserProfiles are created for regular users.
- AdminProfiles are created for superusers.
- The corresponding profiles are saved after any changes to the User instance.
"""

from django.db.models.signals import post_save  # Import post_save signal for user model
from django.dispatch import receiver  # Import the signal receiver decorator
from django.contrib.auth.models import User  # Import the User model
from .models import UserProfile, AdminProfile  # Import custom UserProfile and AdminProfile models

# Signal receiver for creating user profiles after a User instance is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            AdminProfile.objects.get_or_create(user=instance)  # Create AdminProfile if superuser
        else:
            UserProfile.objects.get_or_create(user=instance)  # Create UserProfile for regular users

# Signal receiver for saving user profiles after a User instance is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not instance.is_superuser:
        try:
            profile = instance.userprofile  # Access the related UserProfile instance
            profile.save()  # Save the profile if it exists
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance)  # Create a new UserProfile if it does not exist
