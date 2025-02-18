from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='list'),
    path('novo/', views.create_post, name='create'),
    path('<int:pk>/', views.post_detail, name='detail'),
    path('<int:pk>/editar/', views.edit_post, name='edit_post'),
    path('<int:pk>/excluir/', views.delete_post, name='delete_post'),
    path('<int:post_id>/like/', views.like_post, name='like_post'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('denunciar/<int:pk>/', views.report_content, name='report_content'),
    path('moderacao/', views.moderate_reports, name='moderate_reports'),
    path('moderacao/<int:pk>/', views.resolve_report, name='resolve_report'),
    path('hashtag/<str:hashtag_name>/', views.hashtag_posts, name='hashtag_posts'),
    path('pesquisar/', views.search, name='search'),
]
