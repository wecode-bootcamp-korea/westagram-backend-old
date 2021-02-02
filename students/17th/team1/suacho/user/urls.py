from django.urls import path
from .views      import SingUpView, LogInView

urlpatterns = [
    path('/signup', SingUpView.as_view()),
    path('/login', LogInView.as_view()),
]

