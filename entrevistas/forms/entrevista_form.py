from django import forms
#from ..models import Event

from ..models import EntrevistaEstudante

class EntrevistaEstudanteForm(forms.ModelForm):
    class Meta:
        model = EntrevistaEstudante
        fields = '__all__'

        widgets = {
            # Dados do estudante
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'curso': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'faculdade': forms.Select(attrs={'class': 'form-select'}),
            'faixa_etaria': forms.Select(attrs={'class': 'form-select'}),
            'situacao_profissional': forms.Select(attrs={'class': 'form-select'}),
            'semestre': forms.Select(attrs={'class': 'form-select'}),
            'bairro_residencia': forms.TextInput(attrs={'class': 'form-control'}),

            # Expectativas
            'expectativas_curso': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'receios_curso': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

            # Contactos
            'contacto_estudante_telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'contacto_estudante_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contacto_encarregado_telefone': forms.TextInput(attrs={'class': 'form-control'}),

            # Observações
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'entrevistado_por': forms.TextInput(attrs={'class': 'form-control'}),
        }