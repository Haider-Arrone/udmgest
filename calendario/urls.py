from django.urls import path

from . import views

app_name = 'calendario'

urlpatterns = [
     path("calendario/", views.calendar_view, name="calendario"),
     path("academico/", views.calendar_interno_view, name="calendario_interno"),
     path('events/', views.event_list, name='event-list'),
    path('events/new/', views.event_create, name='event-create'),
    path('api/events/', views.event_list_api, name='event_list_api'),
#     path('create/new', views.cadastrar_actividade,
#          name='cadastrar_actividade'),
#     path('list/', views.listar_actividades, name='listar_actividades'),
#     path('details/<int:id>/', views.detalhes_actividade, name='detalhes_actividade'),
#     path('relatorio/', views.relatorio_actividades, name='relatorio_actividades'),
#     path('search/',
#          views.actividade_search, name="actividade_search"),

]