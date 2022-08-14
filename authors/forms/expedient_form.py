from dataclasses import fields
from django import forms
from expedient.models import Departamento, Expedient
from collections import defaultdict


class AuthorExpedientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        #add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
    
    assunto = forms.CharField(
        error_messages={'required': 'Digite o assunto'},
        label='Assunto',
    ) 
    
    descricao = forms.CharField(
        error_messages={'required': 'Digite a descrição'},
        label='Descrição',
    )    
    anexo = forms.FileField(
        required=False,
        label='Anexo',
    ) 
    
    class Meta:
        model = Expedient
        fields = 'tipo', 'departamento', 'categoria', 'assunto','descricao', 'prioridade', 'confidencial', 'anexo', 
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'tipo': forms.Select(
                choices=(
                    ('Interno', 'Interno'),
                    ('Externo-Saida', 'Externo-Saida'),
                    ('Externo-Entrada', 'Externo-Entrada'),
                ),
            ),
            'categoria': forms.Select(
                choices=(
                    ('Pedido de Credencial', 'Pedido de Credencial'),
                    ('Carta de Estágio', 'Carta de Estágio'),
                    ('Declaração', 'Declaração'),
                ),
            ),
            'prioridade': forms.Select(
                choices=(
                    ('Normal', 'Normal'),
                    ('Urgente', 'Urgente'),
                ),
            ),
            
        }

        
        


