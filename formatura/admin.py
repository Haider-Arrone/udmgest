from django.contrib import admin
from .models import Presenca
from django.utils.html import format_html
from django.utils.timezone import localtime
from .models import Formatura, PontoAgenda

# Register your models here.
@admin.register(Presenca)
class PresencaAdmin(admin.ModelAdmin):
    """
    Configuração profissional para o painel de administração do modelo Presenca.
    Inclui filtros avançados, pesquisa, colunas customizadas e formatação visual.
    """

    list_display = (
        'get_nome_usuario',
        'data_presenca',
        'get_hora_entrada_formatada',
        'get_status_presenca',
        'origem_registo',
        'criado_em',
    )

    list_filter = (
        'data_presenca',
        'origem_registo',
        ('usuario', admin.RelatedOnlyFieldListFilter),
    )

    search_fields = (
        'usuario__username',
        'usuario__first_name',
        'usuario__last_name',
    )

    ordering = ['-data_presenca', 'hora_entrada']
    date_hierarchy = 'data_presenca'
    list_per_page = 25

    readonly_fields = (
        'criado_em',
        'atualizado_em',
        'origem_registo',
    )

    fieldsets = (
        ("Informações do Funcionário", {
            'fields': ('usuario',)
        }),
        ("Registo de Presença", {
            'fields': ('data_presenca', 'hora_entrada', 'origem_registo')
        }),
        ("Auditoria do Sistema", {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )

    def get_nome_usuario(self, obj):
        """Retorna o nome completo do usuário ou username."""
        if obj.usuario:
            nome = f"{obj.usuario.first_name} {obj.usuario.last_name}".strip()
            return nome or obj.usuario.username
        return "—"
    get_nome_usuario.short_description = "Funcionário"
    get_nome_usuario.admin_order_field = "usuario__username"

    def get_hora_entrada_formatada(self, obj):
        """Formata a hora de entrada em formato HH:MM."""
        if obj.hora_entrada:
            hora_local = localtime().replace(hour=obj.hora_entrada.hour, minute=obj.hora_entrada.minute)
            return hora_local.strftime("%H:%M")
        return "—"
    get_hora_entrada_formatada.short_description = "Hora de Entrada"

    def get_status_presenca(self, obj):
        """Exibe um rótulo colorido indicando se o funcionário chegou no horário ou atrasado."""
        if not obj.hora_entrada:
            return format_html('<span style="color: gray;">Sem registo</span>')

        if obj.is_atrasado():
            return format_html('<span style="color: red; font-weight: bold;">Atrasado</span>')
        return format_html('<span style="color: green; font-weight: bold;">Pontual</span>')
    get_status_presenca.short_description = "Status"

    def has_add_permission(self, request):
        """
        Impede o registo manual de presenças — apenas o dispositivo biométrico
        deve criar novos registos.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """Permite apenas ao superusuário eliminar registos."""
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        """Permite visualizar, mas não alterar registos (somente superusuário pode editar)."""
        if request.user.is_superuser:
            return True
        return False



class PontoAgendaInline(admin.TabularInline):
    model = PontoAgenda
    extra = 0
    # autocomplete_fields = ["departamento", "responsavel"]
    fields = [
    "ordem",
    "titulo",
    "departamento",
    "responsavel",
    "status",
    "prioridade",
    "data_limite",
    "percentual",
    "aprovado",
    ]
    readonly_fields = []
    ordering = ["ordem", "-prioridade"]




@admin.register(PontoAgenda)
class PontoAgendaAdmin(admin.ModelAdmin):
    list_display = [
    "ordem",
    "titulo",
    "formatura",
    "departamento",
    "responsavel",
    "status",
    "prioridade",
    "data_limite",
    "percentual",
    "aprovado",
    "atrasada",
    ]
    list_filter = ["status", "prioridade", "aprovado", "departamento"]
    search_fields = [
    "titulo",
    "descricao",
    "justificativa",
    "comentario_avaliador",
    ]
    ordering = ["ordem", "-prioridade"]
    autocomplete_fields = ["formatura", "responsavel"]
    readonly_fields = ["criado_em",
        "criado_por",
        "atualizado_em",
        "atualizado_por"]


    fieldsets = (
    (
    "Identificação",
    {
    "fields": (
    "formatura",
    "ordem",
    "titulo",
    )
    },
    ),
    (
    "Responsabilidade",
    {
    "fields": (
    "departamento",
    "responsavel",
    )
    },
    ),
    (
    "Estado",
    {
    "fields": (
    "status",
    "prioridade",
    "data_limite",
    "percentual",
    
    )
    },
    ),
    (
    "Detalhes",
    {
    "fields": (
    "descricao",
    "justificativa",
    "anexo",
    )
    },
    ),
    ("Auditoria do Sistema", {
            "classes": ("collapse",),
            "fields": ("criado_em", "criado_por", "atualizado_em", "atualizado_por")
        }),
    (
    "Avaliação",
    {
    "classes": ("collapse",),
    "fields": (
    "aprovado",
    "comentario_avaliador",
    )
    },
    ),
    )    
    
@admin.register(Formatura)
class FormaturaAdmin(admin.ModelAdmin):
    list_display = [
    "titulo",
    "data",
    "local",
    "hora_inicio",
    "hora_fim",
    "publicado",
    "progresso_percentual",
    ]
    search_fields = ["titulo", "descricao", "observacoes", "local"]
    list_filter = ["publicado", "data"]
    inlines = [PontoAgendaInline]
    autocomplete_fields = []
    readonly_fields = ["progresso_percentual", "total_tarefas", "tarefas_concluidas","criado_em",
        "criado_por",
        "atualizado_em",
        "atualizado_por"]
    fieldsets = (
    (
    "Informações Gerais",
    {
    "fields": (
    "titulo",
    "descricao",
    "observacoes",
    "publicado",
    )
    },
    ),
    (
    "Agenda",
    {
    "fields": (
    "data",
    "local",
    "hora_inicio",
    "hora_fim",
    )
    },
    ),
    ("Auditoria do Sistema", {
            "classes": ("collapse",),
            "fields": ("criado_em", "criado_por", "atualizado_em", "atualizado_por")
        }),
    (
    "Estatísticas",
    {
    "classes": ("collapse",),
    "fields": (
    "progresso_percentual",
    "total_tarefas",
    "tarefas_concluidas",
    ),
    },
    ),
    )
        
