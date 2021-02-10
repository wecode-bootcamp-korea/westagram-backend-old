from django.urls import path
from .views      import UserSignupView

urlpatterns = [
    path('/signup', UserSignupView.as_view())
]