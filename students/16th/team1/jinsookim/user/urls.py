from django.urls import path
from user.views import Sign_Up
urlpatterns = [
    path('/sign_up', Sign_Up.as_view())
]