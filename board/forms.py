from django import forms
from .models import Card

class CardCreateForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ["name", "description", "status", "priority", "assignee"]
