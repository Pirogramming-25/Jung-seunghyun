from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('create/', views.post_create, name='create'),
    path('<int:post_id>/update/', views.post_update, name='update'),
    path('<int:post_id>/delete/', views.post_delete, name='delete'),
    path('search/', views.post_search, name='search'),
    path('<int:post_id>/like/', views.like_toggle, name='like'),
    path('<int:post_id>/comment/', views.comment_create, name='comment_create'),
    path('comment/<int:comment_id>/update/', views.comment_update, name='comment_update'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
]