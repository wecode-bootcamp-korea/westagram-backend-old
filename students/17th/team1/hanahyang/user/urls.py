from django.urls import path

from .views import (
                SignupView,
                LoginView,
                FollowView,
                FollowingView,
                FollowerView,
            )

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/login', LoginView.as_view()),
    path('/follow', FollowView.as_view()),
    path('/<str:user_name>/following', FollowingView.as_view()),
    path('/<str:user_name>/follower', FollowerView.as_view()),
]
