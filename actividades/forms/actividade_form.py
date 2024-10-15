from django import forms
from actividades.models import Atividade

class AtividadeForm(forms.ModelForm):
    class Meta:
        model = Atividade
        fields = ['tipo_atividade', 'descricao', 'prazo', 'hora_inicio', 'hora_fim', 'status', 'observacoes', 'dificuldade', 'prioridade']
        exclude = ['data', 'tempo_gasto'] 