from django.urls import path

from .views import SignupView, LoginView, FollowView 

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/login', LoginView.as_view()),
    path('/follow', FollowView.as_view()),
]
