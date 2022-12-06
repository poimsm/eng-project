from django.urls import re_path
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView
)
from users.views import CustomTokenObtainPairView

from .views import *

app_name = 'api'

urlpatterns = [
    # @app public
    re_path(r'hola\/?$', hola, name='hola'),
    re_path(r'short-video\/?$', short_video),
    re_path(r'info-card\/?$', info_card),
    re_path(r'daily-activities-limited\/?$', daily_activities_limited),

    # @app protected    
    re_path(r'sentence\/?$', user_sentences),
    re_path(r'convert-local-sentences\/?$', convert_local_sentences),
    re_path(r'save-local-sentences\/?$', save_local_sentences),
    re_path(r'daily-activities\/?$', daily_activities),
    re_path(r'screen-flow\/?$', screen_flow),

    # @authentication
    re_path(r'user/sign-up\/?$', user_sign_up),
    re_path(r'user/sign-in\/?$', user_sign_in),
    re_path(r'user/data\/?$', user_data),
    re_path(r'token/verify\/?$', TokenVerifyView.as_view()),
    re_path(r'token/refresh\/?', TokenRefreshView.as_view()),
]
