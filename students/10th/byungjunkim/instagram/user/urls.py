
from django.urls import path
from .views import SignInView,SignUpView

urlpatterns = [
    path('/up',SignUpView.as_view()),
    path('/in',SignInView.as_view())
]
