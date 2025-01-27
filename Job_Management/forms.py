from django import forms
from .models import Job, JobApplication

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['full_name', 'email', 'phone', 'resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 5}),
        }

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
