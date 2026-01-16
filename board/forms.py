from dataclasses import field
from _operator import mod
from django.forms.widgets import Widget
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Card, Comment, Attachment

User = get_user_model()

class AdminSetupForm(forms.Form):
    password1 = forms.CharField(label="Admin Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError("Passwords do not match")
        return cleaned

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required = False)

    class Meta:
        model = User
        fields = ("username", "email")


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ["name", "description", "status", "priority", "assignee"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        Widgets = {
            "text": forms.Textarea(attrs={"rows": 3}),
        }

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ["file"]

