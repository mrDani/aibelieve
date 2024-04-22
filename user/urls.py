from django.urls import path
from . import views

from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user_creation/', views.registerUser, name='user_creation'),
    path('change-password/', views.changePassword, name='change-password'),
    path('verify_code/', views.code_verification, name='verify_code'),
    path('resend-otp/', views.resend_otp, name='resend-otp'),
    path('jokes/', views.jokeView, name='jokes'),
    path('motivation/', views.motivationView, name='motivation'),
]
