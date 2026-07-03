from django.urls import path
from . import views

urlpatterns=[
    path('devtools/add/', views.devtool_create, name='devtool_create'),
    path('devtools/', views.devtool_list, name='devtool_list'),
    path('devtools/<int:pk>/', views.devtool_detail, name='devtool_detail'),
    path('devtools/<int:pk>/delete', views.devtool_delete, name='devtool_delete'),
    path('devtools/<int:pk>/edit', views.devtool_update, name='devtool_update'),
    
    path('ideas/add/', views.idea_create, name='idea_create'),
    path('ideas/', views.idea_list, name='idea_list'),
    path('ideas/<int:pk>/', views.idea_detail, name='idea_detail'),
    path('ideas/<int:pk>/delete/', views.idea_delete, name='idea_delete'),
    path('ideas/<int:pk>/edit/', views.idea_update, name='idea_update'),
    
    path('ideas/<int:pk>/star/', views.idea_star_toggle, name='idea_star_toggle'),
    path('ideas/<int:pk>/interest/', views.idea_interest_update, name='idea_interest_update'),
]