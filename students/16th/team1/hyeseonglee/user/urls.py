from django.urls import path,include
from user.views  import SignUpView, LoginView, FollowView

urlpatterns = [
    path('/create',                 SignUpView.as_view()),
    path('/login',                  LoginView.as_view()),

    path('/read/follow',            FollowView.as_view()),
    path('/create/follow/<int:pk>', FollowView.as_view()),
]

