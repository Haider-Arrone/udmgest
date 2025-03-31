from django.contrib import admin

# Register your models here.

from .models import Faculdade, Curso, Semestre, Disciplina, Pauta

# Customização da interface do Admin para o modelo Faculdade
class FaculdadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    list_filter = ('nome',)
    ordering = ('nome',)
    fields = ('nome',)  # Campos a serem exibidos no formulário de edição

# Customização da interface do Admin para o modelo Curso
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome','faculdade' )
    search_fields = ('nome','faculdade')
    list_filter = ('faculdade',)
    ordering = ('nome',)
    fields = ('nome', 'faculdade')  # Campos a serem exibidos no formulário de edição

# Customização da interface do Admin para o modelo Semestre
class SemestreAdmin(admin.ModelAdmin):
    list_display = ('ano', 'semestre')
    search_fields = ('ano',)
    list_filter = ('semestre',)
    ordering = ('ano', 'semestre')
    fields = ('ano', 'semestre')  # Campos a serem exibidos no formulário de edição

# Customização da interface do Admin para o modelo Disciplina
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome','curso' )
    search_fields = ('nome','curso' )
    list_filter = ('nome','curso' )
    ordering = ('nome','curso' )
    fields = ('nome', 'curso' )  # Campos a serem exibidos no formulário de edição

# Customização da interface do Admin para o modelo Pauta
# class PautaAdmin(admin.ModelAdmin):
#     list_display = ('turma', 'disciplina', 'semestre', 'criado_por', 'data_criacao', 'ativo')
#     search_fields = ('turma', 'disciplina__nome', 'semestre__ano', 'criado_por__username')
#     list_filter = ('ativo', 'semestre', 'disciplina', 'criado_por')
#     ordering = ('data_criacao',)
#     list_editable = ('ativo',)  # Permite editar o campo 'ativo' diretamente na lista
#     readonly_fields = ('data_criacao', 'data_modificacao')  # Campos somente leitura
#     fields = (
#         'turma', 'disciplina', 'semestre','docente', 'avaliacao', 'arquivo', 'criado_por', 'modificado_por',
#         'data_criacao', 'data_modificacao', 'ativo'
#     )  # Campos a serem exibidos no formulário de edição
#     date_hierarchy = 'data_criacao'  # Adiciona uma hierarquia de datas para facilitar a navegação
#     autocomplete_fields = ['criado_por', 'modificado_por', 'disciplina',]

class PautaAdmin(admin.ModelAdmin):
    list_display = (
        'turma', 
        'get_disciplina', 
        'get_curso', 
        'get_faculdade', 
        'semestre', 
        'criado_por', 
        'data_criacao', 
        'ativo'
    )
    search_fields = (
        'turma', 
        'disciplina__nome', 
        'semestre__ano', 
        'criado_por__username',
        'faculdade__nome',
        'curso__nome'
    )
    list_filter = (
        'ativo', 
        'semestre', 
        'disciplina', 
        'faculdade', 
        'curso', 
        'criado_por'
    )
    ordering = ('data_criacao',)
    list_editable = ('ativo',)  # Permite editar o campo 'ativo' diretamente na lista
    readonly_fields = ('data_criacao', 'data_modificacao')  # Campos somente leitura
    fields = (
        'turma', 
        'disciplina', 
        'curso', 
        'faculdade', 
        'semestre', 
        'docente', 
        'avaliacao', 
        'arquivo',
        'criado_por', 
        'modificado_por', 
        'data_criacao', 
        'data_modificacao', 
        'ativo'
    )  # Campos a serem exibidos no formulário de edição
    date_hierarchy = 'data_criacao'  # Adiciona uma hierarquia de datas para facilitar a navegação
    autocomplete_fields = ['criado_por', 'modificado_por', 'disciplina', 'curso', 'faculdade']  # Campos autocompletados

    # Métodos para acessar os dados relacionados e exibi-los
    def get_disciplina(self, obj):
        return obj.disciplina.nome if obj.disciplina else 'Sem Disciplina'
    get_disciplina.short_description = 'Disciplina'

    def get_curso(self, obj):
        return obj.curso.nome if obj.curso else 'Sem Curso'
    get_curso.short_description = 'Curso'

    def get_faculdade(self, obj):
        return obj.faculdade.nome if obj.faculdade else 'Sem Faculdade'
    get_faculdade.short_description = 'Faculdade'

# Registrando os modelos no Admin
admin.site.register(Faculdade, FaculdadeAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Semestre, SemestreAdmin)
admin.site.register(Disciplina, DisciplinaAdmin)
admin.site.register(Pauta, PautaAdmin)
