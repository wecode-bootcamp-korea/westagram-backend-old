from django.urls import path

from .views import signup_views

urlpatterns = [
    path('/signup', signup_views.SignUpView.as_view()),
]