from django.contrib import admin
from .models import Atividade

class AtividadeAdmin(admin.ModelAdmin):
    list_display = (
        'funcionario', 
        'tipo_atividade', 
        'status', 
        'prioridade', 
        'dificuldade', 
        'data', 
        'prazo', 
        'hora_inicio', 
        'hora_fim', 
        'tempo_gasto'
    )  # Mostra essas colunas na listagem de atividades

    list_filter = (
        'status', 
        'prioridade', 
        'dificuldade', 
        'tipo_atividade', 
        'funcionario'
    )  # Adiciona filtros no painel de admin

    search_fields = (
        'funcionario__nome_completo', 
        'descricao', 
        'tipo_atividade'
    )  # Permite buscar atividades pelo nome do funcionário, descrição ou tipo

    readonly_fields = ('tempo_gasto', 'data')  # Define tempo_gasto e data como apenas leitura no admin

    fieldsets = (
        (None, {
            'fields': ('funcionario', 'tipo_atividade', 'descricao', 'status')
        }),
        ('Detalhes do Prazo', {
            'fields': ('prazo', 'hora_inicio', 'hora_fim', 'tempo_gasto')
        }),
        ('Prioridade e Dificuldade', {
            'fields': ('prioridade', 'dificuldade', 'observacoes')
        }),
    )  # Organiza os campos no formulário de edição

    def save_model(self, request, obj, form, change):
        """Atualiza o campo `tempo_gasto` ao salvar."""
        if obj.status == 'concluida' and obj.hora_fim:
            obj.tempo_gasto = obj.calcular_tempo_gasto()  # Calcular tempo gasto
        obj.save()

admin.site.register(Atividade, AtividadeAdmin)
