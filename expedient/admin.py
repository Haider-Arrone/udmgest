from django.contrib import admin

from expedient.models import Departamento, Expedient

# Register your models here.
class DepartamentoAdmin(admin.ModelAdmin):
    ...
 
admin.site.register(Departamento, DepartamentoAdmin)

@admin.register(Expedient)
class ExpedientAdmin(admin.ModelAdmin):
    ...
    
