from django.urls import path

from user.views import SignUpView, SignInView

urlpatterns = [
    path('/login', SignInView.as_view()),
    path('/signup', SignUpView.as_view())
]