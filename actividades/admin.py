from django.contrib import admin
from .models import Atividade, TipoAtividade

class AtividadeAdmin(admin.ModelAdmin):
    list_display = (
        'funcionario', 
        'get_departamento',  # Exibe o departamento do funcionário
        'tipo_atividade', 
        'status', 
        'prioridade', 
        'dificuldade', 
        'data', 
        'prazo', 
        'hora_inicio', 
        'hora_fim', 
        'tempo_gasto'
    )

    list_filter = (
        'status', 
        'prioridade', 
        'dificuldade', 
        'tipo_atividade', 
        'funcionario', 
        'funcionario__departamento'  # Filtro adicional para o departamento
    )

    search_fields = (
        'funcionario__nome_completo', 
        'descricao', 
        'tipo_atividade__nome'  # Ajuste para buscar pelo nome do tipo de atividade
    )

    readonly_fields = ('tempo_gasto', 'data')

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
    )

    def get_departamento(self, obj):
        return obj.funcionario.departamento.nome
    get_departamento.short_description = 'Departamento'  # Define o título da coluna no admin

    def save_model(self, request, obj, form, change):
        """Atualiza o campo `tempo_gasto` ao salvar e valida o tipo de atividade conforme o departamento."""
        if obj.tipo_atividade.departamento != obj.funcionario.departamento:
            raise ValueError("O tipo de atividade deve pertencer ao mesmo departamento do funcionário.")
        
        # Calcular tempo gasto se a atividade estiver concluída
        if obj.status == 'concluida' and obj.hora_fim:
            obj.tempo_gasto = obj.calcular_tempo_gasto()
        
        super().save_model(request, obj, form, change)

admin.site.register(Atividade, AtividadeAdmin)

admin.site.register(TipoAtividade)