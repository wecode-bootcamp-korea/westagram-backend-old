from django.urls import path
from .views      import UserSignup, UserSignin

urlpatterns = [
    path('/signup', UserSignup.as_view()),
    path('/signin', UserSignin.as_view())
]