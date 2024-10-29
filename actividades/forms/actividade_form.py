from django import forms
from actividades.models import Atividade, TipoAtividade

class AtividadeForm(forms.ModelForm):
    
    tipo_atividade = forms.ModelChoiceField(
        queryset=TipoAtividade.objects.all(),
        empty_label='Selecione o Tipo de Atividade',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Atividade
        fields = ['tipo_atividade', 'descricao', 'prazo', 'hora_inicio', 'hora_fim', 'status', 'observacoes', 'dificuldade', 'prioridade']
        exclude = ['data', 'tempo_gasto'] 
        widgets = {
            'prazo': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fim': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_atividade'].queryset = TipoAtividade.objects.all()  # Atualiza o queryset