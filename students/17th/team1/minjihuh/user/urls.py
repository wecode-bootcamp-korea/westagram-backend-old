from django.urls import path
from user.views  import ( SignUpView, 
                          SignInView,
                          FollowView
)

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/follow', FollowView.as_view())
]