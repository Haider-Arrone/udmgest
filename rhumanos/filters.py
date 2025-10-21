import django_filters

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from authors.models import Profile
from expedient.models import Funcionario, Departamento



# filters.py

from .models import Curriculo, Idioma, FormacaoAcademica, CursoCertificacao, CompetenciasDigitais, HabilidadesTalentos, MobilidadeInterna

class CurriculoFilter(django_filters.FilterSet):
    """
    Filtro avançado para o modelo Curriculo com todos os campos principais
    e relações associadas (formações, cursos, competências, habilidades e mobilidade interna).
    """

    # --- Campos do usuário ---
    nome = django_filters.CharFilter(
        field_name='user__first_name',
        lookup_expr='icontains',
        label='Nome',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'})
    )
    sobrenome = django_filters.CharFilter(
        field_name='user__last_name',
        lookup_expr='icontains',
        label='Sobrenome',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'})
    )

    # --- Campos principais ---
    cargo_actual = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Cargo Actual',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cargo Actual'})
    )

    regime_contrato = django_filters.ChoiceFilter(
        choices=Curriculo.REGIME_CONTRATO_CHOICES,
        label='Regime de Contrato',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    data_nascimento = django_filters.DateFromToRangeFilter(
        label='Data de Nascimento (intervalo)',
        widget=django_filters.widgets.RangeWidget(attrs={'type': 'date', 'class': 'form-control'})
    )

    naturalidade = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Naturalidade',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Naturalidade'})
    )

    idiomas = django_filters.ModelMultipleChoiceFilter(
        queryset=Idioma.objects.all(),
        label='Idiomas',
        widget=forms.CheckboxSelectMultiple
    )

    contacto_telefonico = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Contacto Telefónico',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+258 82 000 0000'})
    )

    endereco_electronico = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Endereço Electrónico',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email@dominio.com'})
    )

    endereco_fisico = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Endereço Físico',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua, Bairro, Cidade'})
    )

    areas_interesse = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Áreas de Interesse',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Áreas de Interesse'})
    )

    # --- Campos relacionados: Formações, Cursos, Competências, Habilidades, Mobilidade ---
    grau_entrada = django_filters.ChoiceFilter(
        field_name='formacoes__grau_entrada',
        choices=FormacaoAcademica.GRAU_CHOICES,
        label='Grau Académico de Entrada',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    grau_actual = django_filters.ChoiceFilter(
        field_name='formacoes__grau_actual',
        choices=FormacaoAcademica.GRAU_CHOICES,
        label='Grau Académico Actual',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    area_formacao = django_filters.CharFilter(
        field_name='formacoes__area_formacao',
        lookup_expr='icontains',
        label='Área de Formação',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    instituicao_ensino = django_filters.CharFilter(
        field_name='formacoes__instituicao_ensino',
        lookup_expr='icontains',
        label='Instituição de Ensino',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    ano_conclusao_formacao = django_filters.NumberFilter(
        field_name='formacoes__ano_conclusao',
        label='Ano de Conclusão (Formação)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    nome_curso = django_filters.CharFilter(
        field_name='cursos_certificacoes__nome_curso',
        lookup_expr='icontains',
        label='Nome do Curso / Certificação',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    instituicao_formadora = django_filters.CharFilter(
        field_name='cursos_certificacoes__instituicao_formadora',
        lookup_expr='icontains',
        label='Instituição Formadora',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    duracao_curso = django_filters.CharFilter(
        field_name='cursos_certificacoes__duracao',
        lookup_expr='icontains',
        label='Duração do Curso',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    ano_conclusao_curso = django_filters.NumberFilter(
        field_name='cursos_certificacoes__ano_conclusao',
        label='Ano de Conclusão (Curso)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    ferramentas_trabalho = django_filters.ChoiceFilter(
        field_name='competencias_digitais__ferramentas_trabalho',
        choices=CompetenciasDigitais.NIVEL_CHOICES,
        label='Nível em Ferramentas de Trabalho',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    gestao_email = django_filters.ChoiceFilter(
        field_name='competencias_digitais__gestao_email',
        choices=CompetenciasDigitais.SIM_NAO_CHOICES,
        label='Gestão de Email',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    uso_plataformas_ensino = django_filters.ChoiceFilter(
        field_name='competencias_digitais__uso_plataformas_ensino',
        choices=CompetenciasDigitais.SIM_NAO_CHOICES,
        label='Uso de Plataformas de Ensino',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    plataforma_nome = django_filters.CharFilter(
        field_name='competencias_digitais__plataforma_nome',
        lookup_expr='icontains',
        label='Nome da Plataforma',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    uso_redes_sociais = django_filters.ChoiceFilter(
        field_name='competencias_digitais__uso_redes_sociais',
        choices=CompetenciasDigitais.REDES_SOCIAIS_CHOICES,
        label='Uso de Redes Sociais',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    outras_competencias = django_filters.CharFilter(
        field_name='competencias_digitais__outras_competencias',
        lookup_expr='icontains',
        label='Outras Competências',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # Habilidades e talentos
    habilidades_tecnicas = django_filters.ChoiceFilter(
        field_name='habilidades_talentos__habilidades_tecnicas',
        choices=HabilidadesTalentos.HABILIDADES_TECNICAS_CHOICES,
        label='Habilidades Técnicas',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    comunicacionais = django_filters.ChoiceFilter(
        field_name='habilidades_talentos__comunicacionais',
        choices=HabilidadesTalentos.COMUNICACIONAIS_CHOICES,
        label='Habilidades Comunicacionais',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    culturais = django_filters.ChoiceFilter(
        field_name='habilidades_talentos__culturais',
        choices=HabilidadesTalentos.CULTURAIS_CHOICES,
        label='Habilidades Culturais',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    desportivas = django_filters.ChoiceFilter(
        field_name='habilidades_talentos__desportivas',
        choices=HabilidadesTalentos.DESPORTIVAS_CHOICES,
        label='Habilidades Desportivas',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    gastronomicas = django_filters.ChoiceFilter(
        field_name='habilidades_talentos__gastronomicas',
        choices=HabilidadesTalentos.GASTRONOMICAS_CHOICES,
        label='Habilidades Gastronômicas',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    mobilidade_disponibilidade = django_filters.ChoiceFilter(
        field_name='mobilidade_interna__disponibilidade',
        choices=MobilidadeInterna.SIM_NAO_CHOICES,
        label='Disponibilidade para Mobilidade Interna',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    area_interesse_mobilidade = django_filters.CharFilter(
        field_name='mobilidade_interna__area_interesse',
        lookup_expr='icontains',
        label='Área de Interesse para Mobilidade',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Curriculo
        fields = []
        
    

