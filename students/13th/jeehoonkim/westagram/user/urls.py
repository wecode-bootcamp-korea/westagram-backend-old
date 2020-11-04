from django.urls import path
from .utils      import authorize_decorator
from .views      import (
    SignUpView, 
    SignInView, 
    FollowView
)

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/<int:user_id>/follow', FollowView.as_view())
]