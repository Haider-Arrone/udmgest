from collections import defaultdict
from dataclasses import fields

from django import forms
from expedient.models import Departamento, Funcionario, Parecer


class ParecerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

    anexo = forms.FileField(
        required=False,
        label='Anexo',
    )

    id_receptor = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        label='Destinatário',
        widget=forms.Select
    )

    class Meta:
        model = Parecer
        #id_receptor = forms.ModelChoiceField(queryset=Funcionario.objects.filter())

        fields = 'id_receptor', 'descricao', 'anexo',
        widgets = {


            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            # 'id_receptor': forms.ModelChoiceField(queryset=Funcionario.objects.all()),
            'tipo': forms.Select(
                choices=(
                    ('Interno', 'Interno'),
                    ('Externo-Saida', 'Externo-Saida'),
                    ('Externo-Entrada', 'Externo-Entrada'),
                ),
            ),


        }
