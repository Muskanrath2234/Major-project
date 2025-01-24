# User_Management/models.py

from django.db import models  # Import Django's models for database operations
from django.contrib.auth.models import User  # Import the built-in User model

# UserProfile model for managing additional user details
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')  # Link to the built-in User model
    full_name = models.CharField(max_length=100)  # User's full name
    age = models.IntegerField(null=True, blank=True)  # User's age, can be null or blank
    room_number = models.CharField(max_length=10)  # Room number where the user resides
    bed_number = models.CharField(max_length=10)  # Bed number assigned to the user in the room
    mobile_number = models.CharField(max_length=15)  # User's mobile number
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')  # Profile picture with a default image
    aadhar_card = models.CharField(max_length=12, null=True, blank=True)  # User's Aadhar card number, can be null or blank
    pan_card = models.CharField(max_length=10, null=True, blank=True)  # User's PAN card number, can be null or blank
    bio = models.TextField()  # A brief biography or description about the user

    def __str__(self):
        return self.user.username  # String representation of the UserProfile using the associated User's username