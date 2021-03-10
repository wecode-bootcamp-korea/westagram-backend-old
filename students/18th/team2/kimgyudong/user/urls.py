from django.urls import path

from .views import UserSignUp, UserSignIn

urlpatterns = [
   path('/signup', UserSignUp.as_view()),
   path('/signin', UserSignIn.as_view()),
]
