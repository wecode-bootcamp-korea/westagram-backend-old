from django.urls import path
from . views     import UserView, LoginView


urlpatterns = [
        path('', UserView.as_view()),
        path('/login', LoginView.as_view())
        ]
