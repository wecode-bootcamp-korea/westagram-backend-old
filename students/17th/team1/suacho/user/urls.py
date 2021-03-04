from django.urls import path
from .views      import SingUpView, LogInView, FollowView

urlpatterns = [
    path('/signup', SingUpView.as_view()),
    path('/login', LogInView.as_view()),
    path('/follow', FollowView.as_view()),
]

