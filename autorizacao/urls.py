from django.urls import path

from . import views

app_name = 'autorizacao'

urlpatterns = [

    path('create/new', views.cadastrar_autorizacao,
         name='cadastrar_autorizacao'),
    path('list/', views.listar_autorizacoes, name='listar_autorizacoes'),
    path('details/<int:id>/', views.detalhes_autorizacao, name='detalhes_autorizacao'),

]