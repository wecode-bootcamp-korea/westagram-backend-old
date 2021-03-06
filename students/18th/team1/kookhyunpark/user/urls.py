from django.urls import path

from user.views import SignUpView, LoginView

urlpatterns = [
    path('/login', LoginView.as_view()),
    path('/signup', SignUpView.as_view())
]