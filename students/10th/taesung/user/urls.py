from django.urls import path

from .views import SignUp, SignIn

urlpatterns = [
    path('', SignUp.as_view()),
    path('/log', SignIn.as_view())
]
