from django.urls import path

from .views import signup_views, login_views

urlpatterns = [
    path('/signup', signup_views.SignUpView.as_view()),
    path('/login', login_views.LogInView.as_view()),
]