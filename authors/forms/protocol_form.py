from collections import defaultdict
from dataclasses import fields

from django import forms
from expedient.models import Departamento, Protocolo


class AuthorProtocolForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        #add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    observacao = forms.CharField(
        error_messages={'required': 'Digite a observação'},
        label='Observação',
    )
    prazo = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Protocolo
        fields = 'descricao', 'destinatario', 'observacao', 'prazo',
