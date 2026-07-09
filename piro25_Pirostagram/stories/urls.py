from django.urls import path
from . import views

app_name = 'stories'

urlpatterns = [
    path('create/', views.story_create, name='create'),
]