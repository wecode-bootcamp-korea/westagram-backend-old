from django.urls import path
from .views      import SignUpView, SignInView, FollowView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/<int:user_id>', FollowView.as_view()),
]