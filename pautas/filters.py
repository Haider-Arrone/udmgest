import django_filters

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from authors.models import Profile
from expedient.models import Funcionario, Departamento
from .models import Semestre, Pauta, Curso, Disciplina, Faculdade
from django.utils import timezone

from .models import Pauta, Disciplina, Semestre


class PautaFilter(django_filters.FilterSet):
    faculdade = django_filters.ModelChoiceFilter(
        queryset=Faculdade.objects.all(),
        label='Faculdade'
    )
    curso = django_filters.ModelChoiceFilter(
        queryset=Curso.objects.all(),  # Inicialmente vazio
        label='Curso'
    )
    
    
    # Filtro para a disciplina
    disciplina = django_filters.ModelChoiceFilter(
        queryset=Disciplina.objects.all(),  # Inicialmente vazio
        label='Disciplina'
    )

    # Filtro para o semestre
    semestre = django_filters.ModelChoiceFilter(
        queryset=Semestre.objects.all(),
        label='Semestre'
    )

    # Filtro para a avaliação (1º teste, 2º teste, etc.)
    avaliacao = django_filters.ChoiceFilter(
        field_name='avaliacao',
        choices=Pauta.AVALIACAO_CHOICES,
        widget=forms.Select(),
        label='Avaliação'
    )

    # Filtro para a data de criação da pauta
    data_criacao = django_filters.DateFromToRangeFilter(
        field_name='data_criacao',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Data de Criação'
    )

    # Filtro para o status da pauta (ativo ou não)
    # ativo = django_filters.BooleanFilter(
    #     field_name='ativo',
    #     label='Ativo',
    #     widget=forms.CheckboxInput()
    # )
    turma = django_filters.CharFilter(
        field_name='turma',
        lookup_expr='icontains',  # Faz uma busca case-insensitive
        label='Turma',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    docente = django_filters.CharFilter(
        field_name='docente',
        lookup_expr='icontains',  # Faz uma busca case-insensitive
        label='Docente',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Pauta
        fields = [
            'semestre','faculdade','curso', 'disciplina',  'avaliacao', 'data_criacao', 'turma', 'docente',
        ]
    def filter_data_criacao(self, queryset, name, value):
        # Se o valor do filtro não for nulo, converta as datas para "aware"
        if value:
            # Converte para o fuso horário configurado (exemplo: UTC)
            value.start = timezone.make_aware(value.start) if value.start else None
            value.stop = timezone.make_aware(value.stop) if value.stop else None
        
        return super().filter_data_criacao(queryset, name, value)
    