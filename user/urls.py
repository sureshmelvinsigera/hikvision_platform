from django.contrib.auth import views
from django.urls import path

from .views import index

app_name = 'user'
urlpatterns = [
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(), name='index'),
    path('', index, name='index'),
]
