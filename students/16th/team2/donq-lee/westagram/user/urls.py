from django.urls import path
from user.views import UserSignUpView, UserSignInView 

urlpatterns = [
    path('/signup', UserSignUpView.as_view()),
    path('/signin', UserSignInView.as_view()),
]