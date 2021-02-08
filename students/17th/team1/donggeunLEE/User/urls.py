from django.urls import path
from .views      import UserSignUpView, UserlonginView, FollowView

urlpatterns = [
        path('/user', UserSignUpView.as_view()),
        path('/login', UserlonginView.as_view()),
        path('/follow', FollowView.as_view())
    ]
