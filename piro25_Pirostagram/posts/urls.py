from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('create/', views.post_create, name='create'),
    path('<int:post_id>/update/', views.post_update, name='update'),
    path('<int:post_id>/delete/', views.post_delete, name='delete'),
    path('<int:post_id>/like/', views.like_toggle, name='like'),
]