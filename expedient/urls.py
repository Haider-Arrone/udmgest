from django.urls import path

from . import views

app_name = 'expedient'

urlpatterns = [
    path('', views.home, name="home"),
    path('expedients/<int:id>/', views.expedient, name="expedient"),
  #  path('recipes/search/', views.search, name="search"), 
   # path('recipes/category/<int:category_id>/', views.category, name="category"),
   # path('recipes/<int:id>/', views.recipe, name="recipe"),
    
]
