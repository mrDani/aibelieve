from django.urls import path
from . import views
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/password_reset/request/', reset_password_request_token, name='reset_password_request_token'),
    path('api/password_reset/confirm/', reset_password_confirm, name='reset_password_confirm'),


    path('user_creation/', views.registerUser, name='user_creation'),
    path('change-password/', views.changePassword, name='change-password'),
    path('verify_code/', views.code_verification, name='verify_code'),
    path('resend-otp/', views.resend_otp, name='resend-otp'),
<<<<<<< HEAD
    path('jokes/', views.jokeView, name='jokes'),
    path('motivation/', views.motivationView, name='motivation'),
=======
    
>>>>>>> a7d983ff760f3645686ea062f7c5a21b144bfc45
]
