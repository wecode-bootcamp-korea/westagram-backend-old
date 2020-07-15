from django.urls import path

from .views      import SignUp, SignIn

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view())
]
