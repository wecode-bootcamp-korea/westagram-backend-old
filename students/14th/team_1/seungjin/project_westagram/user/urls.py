from django.urls import path
from .views import (
                RegistView,
                LoginView,
                Follow,
                )

urlpatterns=[
        path('/regist', RegistView.as_view()),
        path('/login', LoginView.as_view()),
        path('/follow', Follow.as_view()),
        ]
