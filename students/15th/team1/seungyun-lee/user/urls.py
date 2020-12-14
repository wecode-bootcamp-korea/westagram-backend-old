from django.urls import path
from user.views  import SignupView
from user.views  import SigninView

urlpatterns = [
    path('/signin', SigninView.as_view()),
    path('/signup', SignupView.as_view())

]
