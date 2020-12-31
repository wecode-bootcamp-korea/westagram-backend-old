from django.urls import path

from .views      import RegisterView, LoginView, FollowView

urlpatterns = [
    path('/register', RegisterView.as_view()),
    path('/login',    LoginView.as_view()),
    path('/follow',   FollowView.as_view()),
]