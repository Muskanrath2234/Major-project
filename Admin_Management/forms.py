# Import necessary modules for creating forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.models import ModelForm
from django.forms.widgets import FileInput
from .models import Profile

# This form is for user registration, inheriting from UserCreationForm
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        # Fields to include in the registration form
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            # Customizing form widgets (HTML input elements)
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),  # Placeholder for username
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),  # Placeholder for email
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),  # Placeholder for password
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),  # Placeholder for confirm password
        }
        help_texts = {
            # Removing help text for a cleaner look
            'username': None,  # Removing default help text for username field
            'password1': None,  # Removing default help text for password1 field
            'password2': None,  # Removing default help text for password2 field
        }

    def __init__(self, *args, **kwargs):
        # Customizing form layout and styling
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = None  # Ensuring no help text is shown
            # Applying a custom CSS class for form styling
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',  # Adding Bootstrap's form-control class
            })

# This form is for creating or updating a user profile
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'  # Include all fields from the Profile model
        exclude = ['user']  # Exclude the 'user' field since it is already linked to the User model
        widgets = {
            # Customizing the profile image input widget
            'profile_img': FileInput(),  # This is used to upload profile images
        }
