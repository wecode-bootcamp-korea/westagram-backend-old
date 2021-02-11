from django.urls import path
from user.views import SignUpView, SignIn


urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignIn.as_view())
]