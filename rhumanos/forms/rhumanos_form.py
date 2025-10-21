# forms.py
from django import forms
from django.forms import inlineformset_factory
from ..models import Curriculo, Idioma, FormacaoAcademica, CursoCertificacao, CompetenciasDigitais, HabilidadesTalentos, MobilidadeInterna


class CurriculoForm(forms.ModelForm):
    class Meta:
        model = Curriculo
        fields = [
            'cargo_actual',
            'regime_contrato',
            'data_nascimento',
            'naturalidade',
            'idiomas',
            'contacto_telefonico',
            'endereco_electronico',
            'endereco_fisico',
            'areas_interesse',
            'ficheiro_cv',
        ]
        labels = {
            'cargo_actual': 'Cargo Actual',
            'regime_contrato': 'Regime de Contrato',
            'data_nascimento': 'Data de Nascimento',
            'naturalidade': 'Naturalidade',
            'idiomas': 'Idiomas',
            'contacto_telefonico': 'Contacto Telefónico',
            'endereco_electronico': 'Endereço Electrónico',
            'endereco_fisico': 'Endereço Físico',
            'areas_interesse': 'Áreas de Interesse',
            'ficheiro_cv': 'Ficheiro do CV',
        }
        widgets = {
            'cargo_actual': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Analista de Sistemas'}),
            'regime_contrato': forms.Select(attrs={'class': 'form-select'}),
            'data_nascimento': forms.DateInput(
    attrs={'class': 'form-control', 'type': 'date'},
    format='%Y-%m-%d'
),
            'naturalidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Maputo'}),
            'idiomas': forms.CheckboxSelectMultiple(),
            'contacto_telefonico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+258 82 000 0000'}),
            'endereco_electronico': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@dominio.com'}),
            'endereco_fisico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua, Bairro, Cidade'}),
            'areas_interesse': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Digite suas áreas de interesse...'}),
            'ficheiro_cv': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# Formsets para relacionamentos 1:N
FormacaoFormSet = inlineformset_factory(
    Curriculo,
    FormacaoAcademica,
    fields=['grau_entrada', 'grau_actual', 'area_formacao', 'instituicao_ensino', 'ano_conclusao'],
    extra=1,
    can_delete=True,
    labels={
        'grau_entrada': 'Grau de Entrada',
        'grau_actual': 'Grau Atual',
        'area_formacao': 'Área de Formação',
        'instituicao_ensino': 'Instituição de Ensino',
        'ano_conclusao': 'Ano de Conclusão',
    },
    widgets={
        'grau_entrada': forms.Select(attrs={'class': 'form-select'}),
        'grau_actual': forms.Select(attrs={'class': 'form-select'}),
        'area_formacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Engenharia Informática'}),
        'instituicao_ensino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: UDM'}),
        'ano_conclusao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2025'}),
    }
)

CursoFormSet = inlineformset_factory(
    Curriculo,
    CursoCertificacao,
    fields=['nome_curso', 'instituicao_formadora', 'duracao', 'ano_conclusao'],
    extra=1,
    can_delete=True,
    labels={
        'nome_curso': 'Nome do Curso',
        'instituicao_formadora': 'Instituição Formadora',
        'duracao': 'Duração',
        'ano_conclusao': 'Ano de Conclusão',
    },
    widgets={
        'nome_curso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Curso Python'}),
        'instituicao_formadora': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: UDM'}),
        'duracao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 3 meses'}),
        'ano_conclusao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2025'}),
    }
)

CompetenciasFormSet = inlineformset_factory(
    Curriculo,
    CompetenciasDigitais,
    fields=['ferramentas_trabalho', 'gestao_email', 'uso_plataformas_ensino', 'plataforma_nome', 'uso_redes_sociais', 'outras_competencias'],
    extra=1,
    can_delete=True,
    labels={
        'ferramentas_trabalho': 'Ferramentas de Trabalho',
        'gestao_email': 'Gestão de Email',
        'uso_plataformas_ensino': 'Uso de Plataformas de Ensino',
        'plataforma_nome': 'Nome da Plataforma',
        'uso_redes_sociais': 'Uso de Redes Sociais',
        'outras_competencias': 'Outras Competências',
    },
    widgets={
        'ferramentas_trabalho': forms.Select(attrs={'class': 'form-select'}),
        'gestao_email': forms.Select(attrs={'class': 'form-select'}),
        'uso_plataformas_ensino': forms.Select(attrs={'class': 'form-select'}),
        'plataforma_nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Moodle'}),
        'uso_redes_sociais': forms.Select(attrs={'class': 'form-select'}),
        'outras_competencias': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descreva outras competências...'}),
    }
)

HabilidadesFormSet = inlineformset_factory(
    Curriculo,
    HabilidadesTalentos,
    fields=['habilidades_tecnicas','habilidades_tecnicas_outro','comunicacionais','comunicacionais_outro','culturais','culturais_outro','desportivas','gastronomicas','outras_habilidades'],
    extra=1,
    labels = {
            'habilidades_tecnicas': 'Habilidades Técnicas',
            'habilidades_tecnicas_outro': 'Outras Habilidades Técnicas',
            'comunicacionais': 'Habilidades Comunicacionais',
            'comunicacionais_outro': 'Outras Habilidades Comunicacionais',
            'culturais': 'Habilidades Culturais',
            'culturais_outro': 'Outras Habilidades Culturais',
            'desportivas': 'Habilidades Desportivas',
            'gastronomicas': 'Habilidades Gastronômicas',
            'outras_habilidades': 'Outras Habilidades',
        },
    can_delete=True,
    widgets={
        'habilidades_tecnicas': forms.Select(attrs={'class': 'form-select'}),
        'habilidades_tecnicas_outro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Outro...'}),
        'comunicacionais': forms.Select(attrs={'class': 'form-select'}),
        'comunicacionais_outro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Outro...'}),
        'culturais': forms.Select(attrs={'class': 'form-select'}),
        'culturais_outro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Outro...'}),
        'desportivas': forms.Select(attrs={'class': 'form-select'}),
        'gastronomicas': forms.Select(attrs={'class': 'form-select'}),
        'outras_habilidades': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Outras habilidades...'}),
    }
)

MobilidadeFormSet = inlineformset_factory(
    Curriculo,
    MobilidadeInterna,
    fields=['disponibilidade','area_interesse','experiencia_anterior'],
    extra=1,
    labels = {
            'disponibilidade': 'Disponibilidade',
            'area_interesse': 'Área de Interesse',
            'experiencia_anterior': 'Experiência Anterior',
        },
    can_delete=True,
    widgets={
        'disponibilidade': forms.Select(attrs={'class': 'form-select'}),
        'area_interesse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Departamento de TI'}),
        'experiencia_anterior': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descreva sua experiência...'}),
    }
)