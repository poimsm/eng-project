from django.urls import re_path
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView
)
from users.views import CustomTokenObtainPairView

from .views import *

app_name = 'api'

urlpatterns = [
    # @app
    re_path(r'hola\/?$', hola, name='hola'),
    re_path(r'short-video\/?$', short_video),
    re_path(r'info-card\/?$', info_card),
    re_path(r'sentence\/?$', user_sentences),
    re_path(r'daily-activities\/?$', daily_activities),
    re_path(r'daily-activities-limited\/?$', daily_activities_limited),
    re_path(r'convert-local-sentences\/?$', convert_local_sentences),
    re_path(r'user/screen-flow\/?$', screen_flow),

    # @authentication
    re_path(r'user/sign-up\/?$', user_register),
    re_path(r'user/data\/?$', user_data),
    re_path(r'user/sign-in\/?$', CustomTokenObtainPairView.as_view()),
    re_path(r'token/verify\/?$', TokenVerifyView.as_view()),
    re_path(r'token/refresh\/?', TokenRefreshView.as_view()),
]
