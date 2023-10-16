import django_filters
from .models import Expedient, User
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from authors.models import Profile


class Expedient_filter(django_filters.FilterSet):
    categoria = django_filters.CharFilter(
        field_name='categoria',  # Nome do campo no modelo
        lookup_expr='exact',
        widget=forms.Select(
            choices=[('Pedido de Credencial', 'Pedido de Credencial'),
                     ('Carta de Estágio', 'Carta de Estágio'),
                     ('Declaração', 'Declaração'),
                     ('Outro', 'Outro'),
                     ]),
        label='Categoria'  # Rótulo do campo no formulário
    )
    tipo = django_filters.CharFilter(
        field_name='tipo',  # Nome do campo no modelo
        lookup_expr='exact',
        widget=forms.Select(
            choices=[('Interno', 'Interno'),
                     ('Externo-Saida', 'Externo-Saida'),
                     ('Externo-Entrada', 'Externo-Entrada'), ]),
        label='Tipo'  # Rótulo do campo no formulário
    )

    prioridade = django_filters.CharFilter(
        field_name='prioridade',  # Nome do campo no modelo
        lookup_expr='exact',
        widget=forms.Select(
            choices=[('Normal', 'Normal'),
                     ('Urgente', 'Urgente'), ]),
        label='Prioridade'  # Rótulo do campo no formulário
    )

    estado = django_filters.CharFilter(
        field_name='estado',  # Nome do campo no modelo
        lookup_expr='exact',
        widget=forms.Select(
            choices=[('Novo', 'Novo'),
                     ('Respondido', 'Respondido'),
                     ('Encaminhado', 'Encaminhado'), ]),
        label='Estado'  # Rótulo do campo no formulário
    )

    assunto = django_filters.CharFilter(
        field_name='assunto',  # Nome do campo no modelo
        lookup_expr='icontains',  # icontains faz a busca case-insensitive e parcial
        label='Assunto'  # Rótulo do campo no formulário
    )

    descricao = django_filters.CharFilter(
        field_name='descricao',  # Nome do campo no modelo
        lookup_expr='icontains',  # icontains faz a busca case-insensitive e parcial
        label='Descrição'  # Rótulo do campo no formulário
    )

    nome_completo = django_filters.CharFilter(
        # Caminho para o campo na relação entre modelos
        field_name='usuario__profile__nome_completo',
        # Pode ser 'icontains' para busca parcial (case-insensitive)
        lookup_expr='icontains',
        label='Nome Completo'
    )

    data_emissao = django_filters.DateTimeFilter(
        field_name='data_emissao',
        widget=forms.DateInput(attrs={'type': 'date'}),
        lookup_expr='date__exact',  # Compara apenas as datas
        label='Data de Emissão'
    )

    class Meta:
        model = Expedient
        exclude = ['anexo', 'slug']
        fields = 'tipo', 'departamento', 'categoria', 'assunto', 'descricao', 'prioridade', 'confidencial', 'estado', 'data_emissao',

        '''widgets = {
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
'''
