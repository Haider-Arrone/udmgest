from django import forms
from ..models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title',  'type', 'semester', 'course', 'turma']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
           
            'type': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'turma': forms.TextInput(attrs={'class': 'form-control'}),
        }
