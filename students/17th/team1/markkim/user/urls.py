from django.urls import path
from . views     import SignUpView, LoginView, FollowView


urlpatterns = [
        path('', SignUpView.as_view()),
        path('/login', LoginView.as_view()),
        path('/follow', FollowView.as_view())
        ]
