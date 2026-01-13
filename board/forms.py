from _operator import mod
from django.forms.widgets import Widget
from django import forms
from .models import Card, Comment, Attachment

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

