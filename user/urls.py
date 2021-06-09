from django.contrib.auth import views
from django.urls import path

from .views import index, auth

app_name = 'user'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='index'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/', auth, name='auth'),
    path('', index, name='index'),
]
