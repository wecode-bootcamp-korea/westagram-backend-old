from django.urls import path
from user.views import SignUpIndexView, SignUpView, LoginView

urlpatterns = [
    path('' , SignUpIndexView.as_view()),
    path('/signup', SignUpView.as_view()),
    path('/login' , LoginView.as_view()),
]