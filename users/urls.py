from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Editar perfil deve vir antes do perfil/<str:username>/ para não ser confundido com um username
    path('perfil/editar/', views.profile_edit, name='profile_edit'),
    path('perfil/<str:username>/', views.profile, name='profile'),
    path('perfil/<str:username>/seguir/', views.toggle_follow, name='toggle_follow'),
    path('perfil/<str:username>/seguidores/', views.followers_list, name='followers'),
    path('perfil/<str:username>/seguindo/', views.following_list, name='following'),
    path('buscar/', views.user_list, name='find_users'),
]
