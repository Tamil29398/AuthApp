from django.urls import path
from .views import AuthView,RefreshTokenView,PasswordResetTokenView

urlpatterns=[
    path('token/',AuthView.as_view()),
    path('refresh/',RefreshTokenView.as_view()),
    path('reset_password/',PasswordResetTokenView.as_view())


]