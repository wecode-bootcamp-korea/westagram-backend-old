from django.urls import path
from .views import UserSignup

urlpatterns = [
    path('', UserSignup.as_view())
]
