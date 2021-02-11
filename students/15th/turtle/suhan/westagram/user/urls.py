from django.urls import path
from .views      import UserView, LoginView

urlpatterns = [
    path('/sign-up', UserView.as_view()),
     path('/log-in', LoginView.as_view()),
]
