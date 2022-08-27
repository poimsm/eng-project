from django.urls import include, path
from .views import create_user, hola

app_name = 'api'

urlpatterns = [
    path('create-user/', create_user, name='create-user'),
    path('hola/', hola, name='hola'),
]
