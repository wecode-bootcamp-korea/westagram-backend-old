from django.urls import path

from .views import Register, LogIn

urlpatterns = [
    path('register/', Register.as_view()),
    path('login/', LogIn.as_view()),
]
