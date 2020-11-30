from django.urls import path
from .views import (
                RegistView,
                LoginView,
                FollowUser,
                )

urlpatterns=[
        path('/regist', RegistView.as_view()),
        path('/login', LoginView.as_view()),
        path('/follow', FollowUser.as_view()),
        ]
