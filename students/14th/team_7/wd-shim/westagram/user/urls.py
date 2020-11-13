from django.urls import path

from user.views  import (
    SignUpView,
    SignInView,
    FollowView,
    GetFollowListView,
    GetFollowerListView
)

urlpatterns = [
    path('/signup',          SignUpView.as_view()),
    path('/signin',          SignInView.as_view()),
    path('/follow',          FollowView.as_view()),
    path('/getFollowList',   GetFollowListView.as_view()),
    path('/getFollowerList', GetFollowerListView.as_view())
]