from django.urls import path

from .views import SignIn, LogIn

urlpatterns = [
    path('SignIn/', SignIn.as_view()),
    path('LogIn/', LogIn.as_view()),
]
