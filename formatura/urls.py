from django.urls import path
from . import autocomplete
from . import views

app_name = 'formatura'

urlpatterns = [
     path('create/new', views.upload_presenca,
         name='upload_presenca'),
     path('create/formatura', views.cadastrar_formatura,
         name='cadastrar_formatura'),
     path('editar_formatura/<int:pk>/', views.editar_formatura, name='editar_formatura'),
#      path('apagar_pauta/<int:pauta_id>/', views.apagar_pauta, name='apagar_pauta'),
    path('list/', views.listar_presencas, name='listar_presencas'),
    path('list/formatura', views.listar_formaturas, name='listar_formaturas'),
    path('details/<int:id>/', views.detalhes_formatura, name='detalhes_formatura'),
    path('relatorio/', views.relatorio_presencas, name='relatorio_presencas'),
    # path('departamento-autocomplete/', views.DepartamentoAutocomplete.as_view(), name='departamento-autocomplete'),
    # path('responsavel-autocomplete/', views.ResponsavelAutocomplete.as_view(), name='responsavel-autocomplete'),

#     path('search/',
#          views.pauta_search, name="pauta_search"),
#     path('search/get-cursos/<int:faculdade_id>/', views.get_cursos, name='get_cursos'),
#     path('search/get-disciplinas/<int:curso_id>/', views.get_disciplinas, name='get_disciplinas'),
]