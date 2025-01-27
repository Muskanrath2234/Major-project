from django import forms
from .models import Ticket

"""
This file contains the form definition for creating and updating support tickets in the application.
It uses the Ticket model and provides a structured form interface for users to submit their issues.
"""

# Ticket Form
class TicketForm(forms.ModelForm):
    """
    This class defines the form for creating and updating tickets.
    It includes fields for issue type, custom issue (optional), and a detailed description.
    """

    class Meta:
        # Specifies the associated model for this form
        model = Ticket
        # Fields to be included in the form
        fields = ['issue_type', 'custom_issue', 'description']

        # Customizing the widgets for form fields
        widgets = {
            'issue_type': forms.Select(attrs={  # Dropdown for selecting issue type
                'class': 'form-control',
                'placeholder': 'Select issue type'
            }),
            'custom_issue': forms.TextInput(attrs={  # Input field for custom issues
                'class': 'form-control',
                'placeholder': 'Custom issue (if any)',
                'maxlength': 100
            }),
            'description': forms.Textarea(attrs={  # Textarea for detailed description
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your issue...',
                'maxlength': 500,
                'style': 'resize:none;'
            }),
        }

        # Custom labels for form fields
        labels = {
            'issue_type': 'Issue Type',
            'custom_issue': 'Custom Issue (Optional)',
            'description': 'Issue Description',
        }

