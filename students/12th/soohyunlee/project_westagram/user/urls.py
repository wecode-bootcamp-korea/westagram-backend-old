from django.urls import path
from .views      import SignUpView
from .views      import SignInView

urlpatterns = [
    path('/SignUp', SignUpView.as_view()),
    path('/SignIn', SignInView.as_view())
]
