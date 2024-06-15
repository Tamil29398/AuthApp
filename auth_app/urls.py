from django.urls import path
from .views import AuthView

urlpatterns=[
    path('token/',AuthView.as_view()),
]