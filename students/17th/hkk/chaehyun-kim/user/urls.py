from django.urls import path, include

from .views import UserView, SignInView, FollowView

urlpatterns = [
    path('/signup', UserView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/follow', FollowView.as_view()),
]
