from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # Linking the Profile model to the User model with a one-to-one relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # An optional email field, as User already has an email field
    email = models.EmailField(blank=True, null=True)  # Optional, since User model already has email

    # Contact number of the user (max length is 10 for typical mobile number)
    contact_number = models.CharField(max_length=10, blank=True, null=True)

    # Address of the user
    address = models.CharField(max_length=200, blank=True, null=True)

    # Age of the user (optional field)
    age = models.IntegerField(null=True, blank=True)

    # Profile image with a default image if not uploaded by the user
    profile_img = models.ImageField(default='image/default.jpg', upload_to='media')

    # Return the username when accessing the Profile object as a string
    def __str__(self):
        return self.user.username
