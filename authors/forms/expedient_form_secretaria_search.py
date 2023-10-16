from collections import defaultdict
from dataclasses import fields

from django import forms
from expedient.models import Departamento, Expedient


class AuthorExpedientFormFilter(forms.ModelForm):
    class Meta:
        model = Expedient

        fields = 'tipo', 'departamento', 'categoria', 'assunto', 'descricao', 'prioridade', 'confidencial', 'estado',  # 'data_emissao',
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
                    ('Outro', 'Outro'),
                ),
            ),
            'prioridade': forms.Select(
                choices=(
                    ('Normal', 'Normal'),
                    ('Urgente', 'Urgente'),
                ),
            ),

        }
