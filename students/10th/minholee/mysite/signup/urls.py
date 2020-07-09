from django.urls import path
from .views import SignUp, SignIn

urlpatterns = [
    path('signup', SignUp.as_view()),
    path('signin', SignIn.as_view())
]
