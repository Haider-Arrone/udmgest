from django import forms
#from ..models import Event

from ..models import Convite

class ConfirmarPresencaForm(forms.ModelForm):
    class Meta:
        model = Convite
        fields = ['nome_completo', 'contacto', 'codigo_convite']
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome completo'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu contacto'}),
            'codigo_convite': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Digite o Código do Convite', 'min': 1}),
        }