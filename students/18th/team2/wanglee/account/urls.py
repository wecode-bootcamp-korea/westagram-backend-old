from django.urls import path
from .views      import UserSignup

urlpatterns = [
    path('/signup', UserSignup.as_view())
]