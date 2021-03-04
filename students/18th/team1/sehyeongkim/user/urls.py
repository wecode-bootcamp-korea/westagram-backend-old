from django.urls import path

from user.views import SignUpView

urlpatterns = [
        path('/signup',SignUpView.as_view()),

        ]
