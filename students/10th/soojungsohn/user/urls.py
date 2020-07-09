from django.urls import path

from .views import (
    SignUpView,
    SignInView,
    FollowView,
    UnFollowView
)

urlpatterns = [
    path('/sign-up',SignUpView.as_view()),
    path('/sign-in', SignInView.as_view()),
    path('/follow', FollowView.as_view()),    
    path('/unfollow', UnFollowView.as_view()),
]
