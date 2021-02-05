from django.urls import path

from .views      import SignUpView, LogInView, FollowView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/login', LogInView.as_view()),
    path('/follow', FollowView.as_view())
]
