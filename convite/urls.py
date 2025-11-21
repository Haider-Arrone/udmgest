from django.urls import path

from . import views

app_name = 'convite'

urlpatterns = [
     path('evento/<int:evento_id>/presencas/', views.confirmar_presenca, name='confirmar_presenca'),
    path("convites/", views.listar_convites, name="listar_convites"),
    path('convite/<int:convite_id>/', views.detalhes_convite, name='detalhes_convite'),
    path(
        'evento/gerarconvite/',
        views.gerar_convite,
        name='gerar_convite'
    ),
    path('confirmarpresencaexterna/', views.confirmar_presenca_externa, name='confirmar_presenca_externa'),

    # path('', views.home, name="home"),
    # path('expedients/<int:id>/', views.expedient, name="expedient"),
    #  path('recipes/search/', views.search, name="search"),
    # path('recipes/category/<int:category_id>/', views.category, name="category"),
    # path('recipes/<int:id>/', views.recipe, name="recipe"),

]
