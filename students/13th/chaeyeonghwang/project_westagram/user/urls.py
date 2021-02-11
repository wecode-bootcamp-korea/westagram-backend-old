from django.urls import path
from user.views import SignupView, LoginView, FollowingView

urlpatterns = [
    path('signup',  SignupView.as_view()),
    path('login',   LoginView.as_view()),
    path('follow',  FollowingView.as_view())
]
