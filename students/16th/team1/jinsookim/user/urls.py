from django.urls import path
from user.views import SignUp,Signin, FollowView

urlpatterns = [
    path('/signup', SignUp.as_view()),
    path('/signin', Signin.as_view()),
    path('/follow/<int:follower_id>', FollowView.as_view())
]

