from django.contrib import admin
from .models import Autorizacao

class AutorizacaoAdmin(admin.ModelAdmin):
    list_display = ('estudante_nome', 'avaliacao_nome', 'data_avaliacao', 'autorizado', 'responsavel', 'data_autorizacao')
    list_filter = ('avaliacao_nome', 'autorizado', 'data_avaliacao', 'data_autorizacao')
    search_fields = ('estudante_nome', 'responsavel__nome_completo')  # Pesquisa por nome do estudante e do responsável
    date_hierarchy = 'data_autorizacao'  # Filtro por data
    list_editable = ('autorizado',)  # Permite edição rápida do campo "autorizado"
    ordering = ('-data_autorizacao',)  # Ordena por data de autorização (mais recente primeiro)
    
    fieldsets = (
        (None, {
            'fields': ('estudante_nome', 'avaliacao_nome', 'data_avaliacao', 'autorizado', 'justificativa', 'responsavel')
        }),
        # 'Datas' fieldset removed since data_autorizacao is auto-filled
    )
    
    readonly_fields = ('data_autorizacao',)  # Tornar data_autorizacao somente leitura

admin.site.register(Autorizacao, AutorizacaoAdmin)
