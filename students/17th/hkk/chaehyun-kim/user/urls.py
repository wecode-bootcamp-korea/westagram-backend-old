from django.urls import path, include

from .views import UserView, SignInView

urlpatterns = [
    path('/signup', UserView.as_view()),
    path('/signin', SignInView.as_view())
]
