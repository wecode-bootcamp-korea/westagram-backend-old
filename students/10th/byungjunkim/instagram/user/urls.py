
from django.urls import path
from .views import SignInView,SignUpView,FollowView

urlpatterns = [
    path('/up',SignUpView.as_view()),
    path('/in',SignInView.as_view()),
    path('/follow',FollowView.as_view())
]
