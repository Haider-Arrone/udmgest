from django.contrib import admin

from expedient.models import Departamento, Expedient, Funcionario, Parecer, Protocolo


# Register your models here.
class DepartamentoAdmin(admin.ModelAdmin):
    ...


admin.site.register(Departamento, DepartamentoAdmin)


class ProtocoloAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'remetente', 'destinatario', 'estado', 'prazo', 'data_confirmacao_recepcao', 'confirmacao_user_status')
    list_filter = ('estado', 'prazo', 'data_emissao', ('remetente', admin.RelatedOnlyFieldListFilter), ('destinatario', admin.RelatedOnlyFieldListFilter), 'confirmacao_user_status')
    search_fields = ('descricao', 'remetente__nome', 'destinatario__nome__nome') 
    date_hierarchy = 'data_emissao'
    list_per_page = 20


admin.site.register(Protocolo, ProtocoloAdmin)


class ParecerAdmin(admin.ModelAdmin):
    list_display = ('id','id_expedient', 'descricao', 'id_receptor', 'id_emissor', 'tipo', 'data_envio')
    list_filter = ('tipo', 'data_envio')
    search_fields = ('descricao',)
    date_hierarchy = 'data_envio'
    list_per_page = 20


admin.site.register(Parecer, ParecerAdmin)


class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'numero_telefone', 'estado', 'departamento')
    list_filter = ('estado', 'departamento')
    search_fields = ('nome_completo', 'numero_telefone')


admin.site.register(Funcionario, FuncionarioAdmin)


@admin.register(Expedient)
class ExpedientAdmin(admin.ModelAdmin):
    list_display = ['id', 'numero_Ex', 'departamento', 'categoria',
                    'assunto', 'estado', 'data_emissao', 'data_recepcao', 'confidencial', 'usuario']
    list_display_links = 'numero_Ex', 'id',
    search_fields = 'id', 'numero_Ex', 'departamento', 'assunto',
    'estado', 'prioridade', 'slug',
    list_filter = 'departamento', 'usuario',  'estado', 'prioridade',
    list_per_page = 20
    list_editable = 'confidencial',
    ordering = '-id',
