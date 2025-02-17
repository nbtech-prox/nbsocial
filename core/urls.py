from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('explorar/', views.explore, name='explore'),
    path('pesquisar/', views.search, name='search'),
]
