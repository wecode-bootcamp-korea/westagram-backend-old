from django.urls import path

from .views import signup_views, login_views, follow_views

urlpatterns = [
    path('/signup', signup_views.SignUpView.as_view()),
    path('/login', login_views.LogInView.as_view()),
    path('/follow', follow_views.FollowView.as_view()),
    path('/unfollow', follow_views.UnFollowView.as_view()),
]