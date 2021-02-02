from django.urls import path
from user.views import SignUpView, SignInView

urlpatterns = [
    path('', SignUpView.as_view()),
    path('/login', SignInView.as_view()),
]


