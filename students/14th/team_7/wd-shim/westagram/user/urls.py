from django.urls import path

from user.views  import (
    SignUpView,
    SignInView,
    FollowView,
    GetFollowList,
    GetFollowerList
)

urlpatterns = [
    path('/signup',          SignUpView.as_view()),
    path('/signin',          SignInView.as_view()),
    path('/follow',          FollowView.as_view()),
    path('/getFollowList',   GetFollowList.as_view()),
    path('/getFollowerList', GetFollowerList.as_view())
]