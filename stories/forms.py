# FILE: stories/forms.py

from django import forms
from .models import Story

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'description', 'is_public', 'allow_contributions']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
