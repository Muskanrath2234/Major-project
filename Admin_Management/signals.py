from .models import *
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Signal receiver to create user profile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # If the User instance is newly created, a Profile is created for that user
        Profile.objects.get_or_create(user=instance)

# Signal receiver to save the profile whenever the User instance is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Save the profile of the user after the User instance is saved
    instance.profile.save()
