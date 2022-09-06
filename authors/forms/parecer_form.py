from collections import defaultdict
from dataclasses import fields

from django import forms
from expedient.models import Parecer


class ParecerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        #add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
    
    #descricao = forms.CharFiled(
     #   error_messages={'required': 'Digite a mensagem'},
      #  label='Mensagem',
    #) 
    
   
    anexo = forms.FileField(
        required=False,
        label='Anexo',
    ) 
    
    class Meta:
        model = Parecer
        fields = 'id_receptor', 'descricao', 'anexo', 
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

        
        