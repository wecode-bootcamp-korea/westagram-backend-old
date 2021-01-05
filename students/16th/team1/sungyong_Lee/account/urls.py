from django.urls import path
from .views      import SignUpView, LoginView

urlpatterns = [
    path("/signup", SignUpView.as_view()),
    path("/signin", LoginView.as_view()),
]
