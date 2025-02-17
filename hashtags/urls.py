from django.urls import path
from . import views

app_name = 'hashtags'

urlpatterns = [
    path('', views.hashtag_list, name='list'),
    path('<str:name>/', views.hashtag_detail, name='detail'),
]
