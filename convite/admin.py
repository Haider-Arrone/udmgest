from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from .models import Evento, Convite
from django.utils import timezone


# ==========================
# Inline de Convites no Evento
# ==========================
class ConviteInline(admin.TabularInline):
    model = Convite
    fields = ('nome_completo', 'contacto', 'lugares_reservados', 'status', 'codigo_convite', 'presente_em', 'marcar_presenca_button')
    readonly_fields = ('presente_em', 'marcar_presenca_button')
    extra = 0
    can_delete = False

    def marcar_presenca_button(self, obj):
        if obj.status != Convite.Status.PRESENTE:
            return format_html(
                '<a class="button" href="{}">Marcar Presença</a>',
                f'/admin/eventos/convite/{obj.id}/marcar_presenca/'
            )
        return "Presente"
    marcar_presenca_button.short_description = "Ação"


# ==========================
# Admin do Evento
# ==========================
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data', 'local', 'criado_em', 'total_convites', 'total_presentes')
    search_fields = ('titulo', 'local')
    list_filter = ('data',)
    inlines = [ConviteInline]

    def total_convites(self, obj):
        return obj.convites.count()
    total_convites.short_description = "Total Convites"

    def total_presentes(self, obj):
        return obj.convites.filter(status=Convite.Status.PRESENTE).count()
    total_presentes.short_description = "Presentes"


# ==========================
# Admin do Convite
# ==========================
@admin.register(Convite)
class ConviteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'evento', 'contacto', 'lugares_reservados', 'status', 'presente_em', 'codigo_convite', 'marcar_presenca_action')
    search_fields = ('nome_completo', 'contacto', 'codigo_convite')
    list_filter = ('status', 'evento')
    actions = ['marcar_presenca', 'confirmar_convite']

    readonly_fields = ('presente_em',)

    def marcar_presenca_action(self, obj):
        if obj.status != Convite.Status.PRESENTE:
            return format_html(
                '<a class="button" href="{}">Marcar Presença</a>',
                f'/admin/eventos/convite/{obj.id}/marcar_presenca/'
            )
        return "Presente"
    marcar_presenca_action.short_description = "Ação"

    # ======================
    # Actions do Admin
    # ======================
    def marcar_presenca(self, request, queryset):
        updated = 0
        for convite in queryset:
            if convite.status != Convite.Status.PRESENTE:
                convite.marcar_presenca()
                updated += 1
        self.message_user(request, f"{updated} convites marcados como presente.")
    marcar_presenca.short_description = "Marcar presença selecionados"

    def confirmar_convite(self, request, queryset):
        updated = queryset.update(status=Convite.Status.CONFIRMADO)
        self.message_user(request, f"{updated} convites confirmados.")
    confirmar_convite.short_description = "Confirmar convites selecionados"
