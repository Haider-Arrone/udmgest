import django_filters
from .models import Atividade
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from authors.models import Profile
from expedient.models import Funcionario, Departamento



class ActivityFilter(django_filters.FilterSet):
    departamento = django_filters.ModelChoiceFilter(
        queryset=Departamento.objects.all(),  # Puxando os departamentos completos
        label='Departamento',
        to_field_name='nome'  # Certifique-se de que `nome` existe no modelo Departamento
    )
    
    # Filtro para o tipo de atividade
    tipo_atividade = django_filters.ChoiceFilter(
        field_name='tipo_atividade',
        choices=Atividade.TIPO_ATIVIDADE_CHOICES,
        widget=forms.Select(),
        label='Tipo de Atividade'
    )

    # Filtro para o status da atividade
    status = django_filters.ChoiceFilter(
        field_name='status',
        choices=Atividade.STATUS_CHOICES,
        widget=forms.Select(),
        label='Status'
    )

    # Filtro para a dificuldade
    dificuldade = django_filters.ChoiceFilter(
        field_name='dificuldade',
        choices=Atividade.DIFICULDADE_CHOICES,
        widget=forms.Select(),
        label='Dificuldade'
    )

    # Filtro para a prioridade
    prioridade = django_filters.ChoiceFilter(
        field_name='prioridade',
        choices=Atividade.PRIORIDADE_CHOICES,
        widget=forms.Select(),
        label='Prioridade'
    )

    # Filtro para o prazo da atividade
    prazo = django_filters.DateTimeFromToRangeFilter(
        field_name='prazo',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Prazo (Intervalo de Datas e Horas)'
    )

    # Filtro para a data de criação da atividade
    data = django_filters.DateFromToRangeFilter(
        field_name='data',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Data de Criação (Intervalo de Datas)'
    )

    # Filtro para a hora de início da atividade
    hora_inicio = django_filters.TimeFilter(
        field_name='hora_inicio',
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label='Hora de Início'
    )

    # Filtro para a hora de fim da atividade
    hora_fim = django_filters.TimeFilter(
        field_name='hora_fim',
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label='Hora de Fim'
    )

    # Filtro para o tempo gasto na atividade
    # tempo_gasto = django_filters.DurationFilter(
    #     field_name='tempo_gasto',
    #     label='Tempo Gasto'
    # )

    # Filtro para observações
    observacoes = django_filters.CharFilter(
        field_name='observacoes',
        lookup_expr='icontains',
        label='Observações'
    )

    # Filtro para o funcionário
    funcionario = django_filters.ModelChoiceFilter(
        queryset=Funcionario.objects.all(),  # Puxando os funcionários completos
        label='Funcionário',
        to_field_name='nome_completo'  # Certifique-se de que `nome_completo` existe no modelo Funcionario
    )

    class Meta:
        model = Atividade
        fields = [
            'departamento', 'tipo_atividade', 'status', 'dificuldade', 'prioridade',
            'prazo', 'data', 'hora_inicio', 'hora_fim', 
            'observacoes', 'funcionario'
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se um departamento for selecionado, limitar os funcionários a esse departamento
        if 'departamento' in self.data and self.data['departamento']:
            self.filters['funcionario'].queryset = Funcionario.objects.filter(departamento_id=self.data['departamento'])