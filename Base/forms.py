# Importing required modules from Django
from django import forms
from django.contrib.auth.forms import AuthenticationForm  # For custom login form
from .models import ContactSubmission  # Importing the ContactSubmission model to create the form for contact submissions

# Custom login form to allow user to select their role (user or admin)
class CustomLoginForm(AuthenticationForm):
    user_type = forms.ChoiceField(choices=[('user', 'User'), ('admin', 'Admin')])  # Adding a choice field for selecting user type (either 'user' or 'admin')

# Contact form for handling contact form submissions
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission  # Tying the form to the ContactSubmission model
        fields = ['name', 'email', 'subject', 'message']  # Fields to be included in the contact form
