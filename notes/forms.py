from django import forms
from .models import MyNotes

class NotesForm(forms.ModelForm):

    class Meta:
        model = MyNotes
    
        fields = [
            "title",
            "text",
        ]