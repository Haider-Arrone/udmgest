from django.urls import path

from . import views

app_name = 'pautas'

urlpatterns = [
     path('create/new', views.cadastrar_pauta,
         name='cadastrar_pauta'),
     path('editar_pauta/<int:pauta_id>/', views.editar_pauta, name='editar_pauta'),
     path('apagar_pauta/<int:pauta_id>/', views.apagar_pauta, name='apagar_pauta'),
#     path('list/', views.listar_actividades, name='listar_actividades'),
    path('details/<int:id>/', views.detalhes_pauta, name='detalhes_pauta'),
#     path('relatorio/', views.relatorio_actividades, name='relatorio_actividades'),
    path('search/',
         views.pauta_search, name="pauta_search"),
    path('search/get-cursos/<int:faculdade_id>/', views.get_cursos, name='get_cursos'),
    path('search/get-disciplinas/<int:curso_id>/', views.get_disciplinas, name='get_disciplinas'),
]