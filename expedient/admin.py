from django.contrib import admin

from expedient.models import Departamento, Expedient, Funcionario

# Register your models here.
class DepartamentoAdmin(admin.ModelAdmin):
    ...
 
admin.site.register(Departamento, DepartamentoAdmin)

class FuncionarioAdmin(admin.ModelAdmin):
    ...
 
admin.site.register(Funcionario, FuncionarioAdmin)

@admin.register(Expedient)
class ExpedientAdmin(admin.ModelAdmin):
    list_display = ['id', 'numero_Ex', 'departamento', 'categoria',
                    'assunto', 'estado', 'data_emissao','confidencial', 'usuario']
    list_display_links = 'numero_Ex', 'id', 
    search_fields = 'id', 'numero_Ex', 'departamento', 'assunto',
    'estado', 'prioridade', 'slug',
    list_filter = 'departamento', 'usuario',  'estado', 'prioridade',
    list_per_page = 20
    list_editable = 'confidencial',
    ordering = '-id',
    
