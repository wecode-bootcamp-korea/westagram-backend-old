from django.urls import path
from .views import SignUpView, LogInView, TokenCheckView

urlpatterns = [
    path("", SignUpView.as_view()),
    path("/login", LogInView.as_view()),
    path("/tokencheck", TokenCheckView.as_view()),
]
