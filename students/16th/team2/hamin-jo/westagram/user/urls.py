from django.urls import path

from user.views import LoginView, SigninView

urlpatterns=[
    path('', SigninView.as_view()),
    path('/login', LoginView.as_view())
]