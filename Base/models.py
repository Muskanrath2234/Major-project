# Importing required modules from Django
from django.db import models

# Subscription model to store user email subscriptions
class Subscription(models.Model):
    email = models.EmailField(unique=True)  # The email field is unique, meaning no duplicate emails allowed

    def __str__(self):
        return self.email  # This will return the email address as the string representation of the object


# ContactSubmission model to store contact form submissions
class ContactSubmission(models.Model):
    name = models.CharField(max_length=255)  # Name of the person submitting the form, with a max length of 255 characters
    email = models.EmailField(unique=True)  # Email field is unique to avoid duplicate entries
    subject = models.CharField(max_length=255)  # Subject of the contact message
    message = models.TextField()  # The actual message from the user
    submitted_at = models.DateTimeField(auto_now_add=True)  # This field automatically records the time when the submission is made

    def __str__(self):
        return f"{self.name} - {self.email}"  # This will return a string in the format "Name - Email" for easy identification
