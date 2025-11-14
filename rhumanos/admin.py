from django.contrib import admin
from .models import (
    Curriculo,
    FormacaoAcademica,
    CursoCertificacao,
    CompetenciasDigitais,
    HabilidadesTalentos,
    MobilidadeInterna,
    Idioma,
)

# --- Inlines --- #

class FormacaoAcademicaInline(admin.TabularInline):
    model = FormacaoAcademica
    extra = 1
    show_change_link = True
    fields = ('grau_entrada', 'grau_actual', 'area_formacao', 'instituicao_ensino', 'ano_conclusao','criado_por', 'atualizado_por', 'criado_em', 'atualizado_em')
    readonly_fields = ('criado_por', 'atualizado_por', 'criado_em', 'atualizado_em')
    ordering = ('-ano_conclusao',)

class CursoCertificacaoInline(admin.TabularInline):
    model = CursoCertificacao
    extra = 1
    show_change_link = True
    fields = ('nome_curso', 'instituicao_formadora', 'duracao', 'ano_conclusao','criado_por', 'atualizado_por', 'criado_em', 'atualizado_em')
    readonly_fields = ('criado_por', 'atualizado_por', 'criado_em', 'atualizado_em')
    ordering = ('-ano_conclusao',)

class CompetenciasDigitaisInline(admin.TabularInline):
    model = CompetenciasDigitais
    extra = 1
    show_change_link = True
    fields = (
        'ferramentas_trabalho', 'gestao_email', 'uso_plataformas_ensino',
        'plataforma_nome', 'uso_redes_sociais', 'outras_competencias', 'criado_por', 'atualizado_por', 'criado_em', 'atualizado_em'
    )
    readonly_fields = ('criado_por', 'atualizado_por', 'criado_em', 'atualizado_em')

class HabilidadesTalentosInline(admin.TabularInline):
    model = HabilidadesTalentos
    extra = 1
    show_change_link = True
    fields = (
        'habilidades_tecnicas', 'habilidades_tecnicas_outro',
        'comunicacionais', 'comunicacionais_outro',
        'culturais', 'culturais_outro',
        'desportivas', 'gastronomicas', 'outras_habilidades', 'criado_por', 'atualizado_por', 'criado_em', 'atualizado_em'
    )
    readonly_fields = ('criado_por', 'atualizado_por', 'criado_em', 'atualizado_em')

class MobilidadeInternaInline(admin.TabularInline):
    model = MobilidadeInterna
    extra = 1
    show_change_link = True
    fields = ('disponibilidade', 'area_interesse', 'experiencia_anterior', 'criado_por', 'atualizado_por', 'criado_em', 'atualizado_em')
    readonly_fields = ('criado_por', 'atualizado_por', 'criado_em', 'atualizado_em')

# --- Admin Principal --- #

@admin.register(Curriculo)
class CurriculoAdmin(admin.ModelAdmin):
    list_display = ('user', 'cargo_actual', 'regime_contrato','get_idiomas', 'contacto_telefonico', 'data_registo')
    list_filter = ('regime_contrato', 'idiomas', 'data_registo')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'cargo_actual', 'endereco_electronico')
    ordering = ('user__username',)
    readonly_fields = ('data_registo','criado_por', 'atualizado_por')
    
    filter_horizontal = ('idiomas',)
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('user', 'cargo_actual', 'regime_contrato', 'data_nascimento', 'naturalidade', 'idiomas')
        }),
        ('Contato', {
            'fields': ('contacto_telefonico', 'endereco_electronico', 'endereco_fisico')
        }),
        ('Áreas de Interesse', {
            'fields': ('areas_interesse',)
        }),
        ('Ficheiro CV', {
            'fields': ('ficheiro_cv',)
        }),
        ('Informações do Sistema', {
            'fields': ('data_registo','criado_por', 'atualizado_por')
        }),
    )

    inlines = [
        FormacaoAcademicaInline,
        CursoCertificacaoInline,
        CompetenciasDigitaisInline,
        HabilidadesTalentosInline,
        MobilidadeInternaInline
    ]
    
    def get_idiomas(self, obj):
        return ", ".join([i.nome for i in obj.idiomas.all()])
    get_idiomas.short_description = "Idiomas"

@admin.register(Idioma)
class IdiomaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)