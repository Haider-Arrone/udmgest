from django.contrib import admin

# Register your models here.

from salas.models import Sala, Ocupacao

# Register your models here.

class OcupacaoAdmin(admin.ModelAdmin):
    list_display = ['sala', 'estado', 'hora_inicio', 'hora_fim', 'turno', 'faculdade', 'display_info']

    def display_info(self, obj):
        return f"{obj.sala.nome} ({obj.estado})"
    display_info.short_description = 'Informação'

admin.site.register(Ocupacao, OcupacaoAdmin)

admin.site.register(Sala)

