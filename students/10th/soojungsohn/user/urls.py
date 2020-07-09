from django.urls import path

from .views import (
    SignUpView,
    SignInView,
    FollowView
)

urlpatterns = [
    path('',SignUpView.as_view()),
    path('signin/', SignInView.as_view()),
    path('follow/', FollowView.as_view()),    
]
