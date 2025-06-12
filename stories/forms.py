# FILE: stories/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Story, Chapter, Rating, UserProfile, Comment

# -----------------------------------------------------------
# ------------------ Form for creating/editing Story model


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ["title", "description", "image", "is_public", "allow_contributions"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }


# -----------------------------------------------------------
# ------------------ Form for creating/editing Chapter model


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ["title", "content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 6}),
        }


# -----------------------------------------------------------
# ------------------ User registration form


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


# -----------------------------------------------------------
# ------------------ Form for rating a chapter (1–5 stars)


class RatingForm(forms.ModelForm):
    value = forms.ChoiceField(
        choices=[(i, "★" * i) for i in range(1, 6)],
        widget=forms.RadioSelect,
        label="Rank this chapter",
    )

    class Meta:
        model = Rating
        fields = ["value"]


# -----------------------------------------------------------
# ------------------ Form for editing user profile info


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["profile_image", "full_name", "about", "contact_email"]


# -----------------------------------------------------------
# ------------------ Form for adding a comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 2, "placeholder": "Add a comment..."}
            )
        }
