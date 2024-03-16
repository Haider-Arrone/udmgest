from django.contrib import admin
from authors.models import Profile

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'numero_telefone', 'estudante_interno', 'instituicao', 'codigo_estudante')
    list_filter = ('estudante_interno', 'instituicao')
    search_fields = ('nome_completo', 'numero_telefone')
