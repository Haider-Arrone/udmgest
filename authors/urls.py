from django.urls import path

from . import views

app_name = 'authors' 
 
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashbord/', views.dashbord, name='dashbord'),
    path('dashbord/expedient/<int:id>/edit/',
         views.dashbord_expedient_edit,
         name='dashbord_expedient_edit'),
    path('dashbord/expedient/<int:id>/see/',
         views.dashbord_expedient_see,
         name='dashbord_expedient_see'),
    path('dashbord/expedient/new', views.dashbord_expedient_new, name='dashbord_expedient_new'),
    path('dashbord/expedient/emitidos', views.dashbord_expedient_emitidos, name='dashbord_expedient_emitidos'),
    path('dashbord/expedient/recebidos', views.dashbord_expedient_recebidos, name='dashbord_expedient_recebidos'),
    path('dashbord/expedient/recebidos_funcionario', views.dashbord_expedient_recebidos_funcionario, name='dashbord_expedient_recebidos_funcionario'),
    path('dashbord/expedient/<int:id>/detail/',
         views.dashbord_expedient_detail,
         name='dashbord_expedient_detail'),
    path('dashbord/expedient/<int:id>/parecer', views.dashbord_expedient_parecer, name='dashbord_expedient_parecer'),
]

