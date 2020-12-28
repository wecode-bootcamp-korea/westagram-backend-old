from django.urls import path
from user.views  import SignupView,SigninView,FollowsView

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/signin', SigninView.as_view()),
    path('/follow/<int:user_pk>',FollowsView.as_view()),
]
