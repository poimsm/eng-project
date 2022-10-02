from django.urls import re_path
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView
)
from users.views import CustomTokenObtainPairView

from .views import *

app_name = 'api'

urlpatterns = [
    re_path(r'hola\/?$', hola, name='hola'),
    re_path(r'get-post\/?$', get_post, name='get-post'),

    re_path(r'sentence\/?$', user_sentences),
    re_path(r'daily-activities\/?$', daily_activities),

    re_path(r'user/fake-user\/?$', create_fake_user),
    re_path(r'user/register\/?$', user_register),
    re_path(r'user/data\/?$', user_data),
    re_path(r'user/sign-in\/?$', CustomTokenObtainPairView.as_view()),    
    re_path(r'token/verify\/?$', TokenVerifyView.as_view()),
    re_path(r'token/refresh\/?', TokenRefreshView.as_view()),
]
