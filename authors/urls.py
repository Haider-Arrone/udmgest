from . import views
from django.urls import path
 
app_name = 'authors' 
 
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='create'),
]

