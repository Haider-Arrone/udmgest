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
        widget=forms.TextInput(attrs={'placeholder': 'Exemplo: Diurno A', 'class': 'form-control'}),
        required=True
    )
    
    disciplina = forms.ModelChoiceField(
        queryset=Disciplina.objects.none(),  # Será atualizado no __init__
        empty_label="Selecione a Disciplina",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.none(),  # Será atualizado no __init__
        empty_label="Selecione o Curso",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    faculdade = forms.ModelChoiceField(
        queryset=Faculdade.objects.all(),
        empty_label="Selecione a Faculdade",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    semestre = forms.ModelChoiceField(
        queryset=Semestre.objects.all(),
        empty_label="Selecione o Semestre",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    avaliacao = forms.ChoiceField(
        choices=Pauta.AVALIACAO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    arquivo = forms.FileField(
        
        widget=forms.ClearableFileInput(attrs={'multiple': False}),
        required=True
    )
    
    docente = forms.CharField(
        
        widget=forms.TextInput(attrs={'placeholder': 'Nome do Docente', 'class': 'form-control'}),
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Se houver uma faculdade selecionada, filtrar os cursos e disciplinas disponíveis
        if 'instance' in kwargs and kwargs['instance']:
            self.fields['curso'].queryset = Curso.objects.filter(faculdade=kwargs['instance'].faculdade)
            self.fields['disciplina'].queryset = Disciplina.objects.filter(curso=kwargs['instance'].curso)
        else:
            self.fields['curso'].queryset = Curso.objects.all()
            self.fields['disciplina'].queryset = Disciplina.objects.all()

    def clean_arquivo(self):
        arquivo = self.cleaned_data.get('arquivo', None)
        if arquivo:
            extensao = arquivo.name.split('.')[-1].lower()
            if extensao not in ['pdf', 'doc', 'docx']:
                raise forms.ValidationError("Apenas arquivos PDF ou Word são permitidos.")
        return arquivo