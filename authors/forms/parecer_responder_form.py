from collections import defaultdict
from dataclasses import fields

from django import forms
from expedient.models import Funcionario, Parecer


class Parecer_Responder_Form(forms.ModelForm):
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
        id_receptor = forms.ModelChoiceField(queryset=Funcionario.objects.filter())
        
        fields =  'descricao', 'anexo', 
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
           
            
        }
        
    


