from django.urls import path

from .views import index

app_name = 'reset'
urlpatterns = [
    path('', index, name='main')
]
