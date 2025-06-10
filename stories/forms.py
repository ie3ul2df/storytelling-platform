# FILE: stories/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Story, Chapter, Rating, UserProfile

# -----------------------------------------------------------

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'description', 'image', 'is_public', 'allow_contributions']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

# -----------------------------------------------------------

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }

# -----------------------------------------------------------

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

# -----------------------------------------------------------

class RatingForm(forms.ModelForm):
    value = forms.ChoiceField(
        choices=[(i, '★' * i) for i in range(1, 6)],
        widget=forms.RadioSelect,
        label="Rank this chapter"
    )

    class Meta:
        model = Rating
        fields = ['value']

# -----------------------------------------------------------

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'full_name', 'about', 'contact_email']

