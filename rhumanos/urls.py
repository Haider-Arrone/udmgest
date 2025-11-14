from django.urls import path

from . import views

app_name = 'rhumanos'

urlpatterns = [
    path('create/new', views.cadastrar_curriculo,
        name='cadastrar_curriculo'),
    path('editar/<int:id>/', views.editar_curriculo, name='editar_curriculo'),
#      path('apagar_pauta/<int:pauta_id>/', views.apagar_pauta, name='apagar_pauta'),
    path('list/', views.listar_curriculos, name='listar_curriculos'),
    path('details/<int:id>/', views.detalhes_curriculo, name='detalhes_curriculo'),
# #     path('relatorio/', views.relatorio_actividades, name='relatorio_actividades'),
    path('search/',
         views.curriculo_search, name="curriculo_search"),
#     path('search/get-cursos/<int:faculdade_id>/', views.get_cursos, name='get_cursos'),
#     path('search/get-disciplinas/<int:curso_id>/', views.get_disciplinas, name='get_disciplinas'),
    # path("seed-curriculos/", views.seed_curriculos_view, name="seed_curriculos"),
]