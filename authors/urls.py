from . import views
from django.urls import path
 
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
    path('dashbord/expedient/new', views.dashbord_expedient_new, name='dashbord_expedient_new'),
]

