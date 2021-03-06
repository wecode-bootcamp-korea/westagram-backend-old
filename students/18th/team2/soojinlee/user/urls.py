from django.urls import path
from .views import UserSignup, UserLogin

urlpatterns = [
    path('', UserSignup.as_view()),
    path('/signin', UserLogin.as_view())
]
