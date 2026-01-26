from django.contrib import admin
from .models import EntrevistaEstudante


@admin.register(EntrevistaEstudante)
class EntrevistaEstudanteAdmin(admin.ModelAdmin):

    # ==================================================
    # LISTAGEM (LIST VIEW)
    # ==================================================
    list_display = (
        'nome',
        'curso',
        'faculdade',
        'semestre',
        'situacao_profissional',
        'suporte_despesas',
        'entrevistado_por',
        'data_entrevista',
    )

    list_filter = (
        'faculdade',
        'situacao_profissional',
        'semestre',
        'suporte_despesas',
        'data_entrevista',
    )

    search_fields = (
        'nome',
        'curso',
        'bairro_residencia',
        'contacto_estudante_telefone',
        'contacto_estudante_email',
        'entrevistado_por',
        'motivo_escolha_curso',
        'motivo_escolha_udm',
        'como_conheceu_udm',
    )

    ordering = ('-data_entrevista',)
    date_hierarchy = 'data_entrevista'
    list_per_page = 25
    save_on_top = True

    # ==================================================
    # FORMULÁRIO (DETAIL VIEW)
    # ==================================================
    fieldsets = (

        ('1. Dados do Estudante', {
            'fields': (
                'nome',
                'curso',
                'genero',
                'faculdade',
                'faixa_etaria',
                'situacao_profissional',
                'semestre',
                'bairro_residencia',
            )
        }),

        ('2. Motivo da Escolha do Curso', {
            'fields': (
                'motivo_escolha_curso',
            ),
            'classes': ('collapse',),
        }),

        ('3. Motivo da Escolha da UDM', {
            'fields': (
                'motivo_escolha_udm',
            ),
            'classes': ('collapse',),
        }),

        ('4. Como Conheceu a UDM', {
            'fields': (
                'como_conheceu_udm',
            ),
            'classes': ('collapse',),
        }),

        ('5. Suporte das Despesas', {
            'fields': (
                'suporte_despesas',
            ),
        }),

        ('6. Expectativas e Receios', {
            'fields': (
                'expectativas_curso',
                'receios_curso',
            ),
            'classes': ('collapse',),
        }),

        ('7. Avaliação Geral do Candidato (1–10)', {
            'fields': (
                'avaliacao_apresentacao',
                'avaliacao_conhecimento_curso',
                'avaliacao_conhecimento_udm',
                'avaliacao_fluencia_comunicativa',
                'avaliacao_objetivos_pessoais',
            ),
        }),

        ('8. Contactos', {
            'fields': (
                'contacto_estudante_telefone',
                'contacto_estudante_email',
                'contacto_encarregado_telefone',
            ),
        }),

        ('9. Observações da Entrevista', {
            'fields': (
                'observacoes',
                'entrevistado_por',
            ),
        }),

        ('Informação do Sistema', {
            'fields': (
                'data_entrevista',
            ),
        }),
    )

    # ==================================================
    # CAMPOS APENAS DE LEITURA
    # ==================================================
    readonly_fields = (
        'data_entrevista',
    )
