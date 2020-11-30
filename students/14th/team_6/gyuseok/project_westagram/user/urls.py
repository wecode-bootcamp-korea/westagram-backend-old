from django.urls import path
from .views import SignUpView, LoginView, DummyView

urlpatterns = [
    path('/signup',SignUpView.as_view()),
    path('/login',LoginView.as_view()),
    path('/dummy',DummyView.as_view()),
]
