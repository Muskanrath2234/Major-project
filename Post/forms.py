from django import forms
from .models import User_Post

class PostForm(forms.ModelForm):
    class Meta:
        model = User_Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter the post title',
                'class': 'form-control',
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Enter the post content',
                'class': 'form-control',
                'rows': 5,
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'title': 'Post Title',
            'content': 'Post Content',
            'image': 'Post Image',
        }

class SearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label='Search Query',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your search query here',
            'class': 'form-control',
        })
    )
    start_date = forms.DateField(
        required=False,
        label='Start Date',
        widget=forms.TextInput(attrs={
            'type': 'date',
            'class': 'form-control',
        })
    )
    end_date = forms.DateField(
        required=False,
        label='End Date',
        widget=forms.TextInput(attrs={
            'type': 'date',
            'class': 'form-control',
        })
    )
