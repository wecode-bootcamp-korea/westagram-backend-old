from django.urls import path, include

from .views import UserView, SignInView, FollowView, FollowDetailView

urlpatterns = [
    path('/signup', UserView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/follow', FollowView.as_view()),
    path('/follow/<int:user_id>', FollowDetailView.as_view()),
]
