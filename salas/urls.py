from django.urls import path

from . import views

app_name = 'salas'

urlpatterns = [
    path('dashbord/', views.consulta_sala,
            name='consulta_sala'),
    path('dashbord/salas/<int:id>/detail/',
         views.dashbord_salas_detail,
         name='dashbord_salas_detail'),
    path('dashbord/salas/search/',
         views.salas_search, name="salas_search"),
]