from django.urls import path

from .views  import SignUp, LogIn

urlpatterns = [
    path('signup/', SignUp.as_view()),
    path('login/', LogIn.as_view())
]