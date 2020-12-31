from django.urls import path

from user.views import SignUpView, LogInView

urlpatterns = [
    path('/sign-up', SignUpView.as_view()),
    path('/log-in' , LogInView.as_view())
]
