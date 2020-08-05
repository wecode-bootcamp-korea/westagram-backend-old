from django.urls import path
from .views  import Signup

urlpatterns = [
    path('signuplist', Signup.as_view())
]
