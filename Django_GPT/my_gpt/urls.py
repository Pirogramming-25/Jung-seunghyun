from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path("", lambda request: redirect("sentiment")),
    path("sentiment/", views.sentiment_view, name="sentiment"),
    path("sentiment/run/", views.sentiment_run, name="sentiment_run"),
    path("summarize/", views.summarize_view, name="summarize"),
    path("summarize/run/", views.summarize_run, name="summarize_run"),
    path("moderate/", views.moderate_view, name="moderate"),
    path("moderate/run/", views.moderate_run, name="moderate_run"),
]

