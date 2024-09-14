from django import forms
from autorizacao.models import Autorizacao

class AutorizacaoForm(forms.ModelForm):
    class Meta:
        model = Autorizacao
        fields = ['estudante_nome', 'avaliacao_nome', 'disciplina', 'data_avaliacao', 'autorizado', 'justificativa', ]
        labels = {
            'data_avaliacao': 'Data da Avaliação (dd/mm/aaaa)',  # Personalize o label do campo aqui
        }