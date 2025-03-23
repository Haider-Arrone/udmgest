from django import forms
from django.contrib.auth import get_user_model
from ..models import Pauta, Disciplina, Semestre, Faculdade, Curso

User = get_user_model()

class PautaForm(forms.ModelForm):
    class Meta:
        model = Pauta
        fields = [
               'semestre', 
            'faculdade',
            'curso', 
            
            'disciplina', 
            'turma', 
             
            
            'docente', 
            'avaliacao', 
            'arquivo', 
        ]
    
    # Customizando widgets para campos específicos
    turma = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Exemplo: Diurno A', 'class': 'form-control'})
    )
    
    disciplina = forms.ModelChoiceField(
        queryset=Disciplina.objects.all(),
        empty_label="Selecione a Disciplina",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(),
        empty_label="Selecione o Curso",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    faculdade = forms.ModelChoiceField(
        queryset=Faculdade.objects.all(),
        empty_label="Selecione a Faculdade",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    semestre = forms.ModelChoiceField(
        queryset=Semestre.objects.all(),
        empty_label="Selecione o Semestre",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    avaliacao = forms.ChoiceField(
        choices=Pauta.AVALIACAO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    arquivo = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': False})
    )
    
    docente = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Nome do Docente', 'class': 'form-control'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        # Validações personalizadas, se necessário
        return cleaned_data