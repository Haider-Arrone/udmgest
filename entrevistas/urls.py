from django.urls import path

from . import views

app_name = 'entrevistas'

urlpatterns = [
    #  path('evento/<int:evento_id>/presencas/', views.confirmar_presenca, name='confirmar_presenca'),
    path("list/", views.listar_entrevistas, name="listar_entrevistas"),
    path('<int:entrevista_id>/', views.detalhes_entrevista, name='detalhes_entrevista'),
    path("estatisticas/", views.estatisticas_entrevistas, name="estatisticas_entrevistas"),
    path("graficos/", views.estatisticas_entrevistas_grafico, name="estatisticas_entrevistas_grafico"),
    path('register/', views.cadastrar_entrevista, name='cadastrar_entrevista'),
    #path('register/interna', views.cadastrar_entrevista, name='cadastrar_entrevista_interna'),
    path('', views.entrevista_externa, name='entrevista_externa'),
    path('ri', views.entrevista_interna, name='entrevista_interna'),
    path("entrevistas/<int:entrevista_id>/editar-avaliacao/",
    views.editar_avaliacao_entrevista,
    name="editar_avaliacao_entrevista"
),
    path(
    "entrevista/<int:entrevista_id>/anular/",
    views.anular_entrevista,
    name="anular_entrevista"
),
    # path("convite/editar/<int:convite_id>/", views.editar_convite, name="editar_convite"),
    # path('', views.home, name="home"),
    # path('expedients/<int:id>/', views.expedient, name="expedient"),
    #  path('recipes/search/', views.search, name="search"),
    # path('recipes/category/<int:category_id>/', views.category, name="category"),
    # path('recipes/<int:id>/', views.recipe, name="recipe"),

]
