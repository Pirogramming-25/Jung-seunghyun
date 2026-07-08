from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('<str:username>/follow/', views.follow_toggle, name='follow'),
    path('<str:username>/', views.profile, name='profile')
]