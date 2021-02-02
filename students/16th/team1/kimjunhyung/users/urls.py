from django.urls import path

from .views import UserSignUpView, UserSignInView, FollowUser

urlpatterns = [
    path("/signup", UserSignUpView.as_view()),
    path("/signin", UserSignInView.as_view()),
    path("/follow", FollowUser.as_view())
]
