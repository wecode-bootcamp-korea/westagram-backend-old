from django.urls import path
from .views      import UserSignUpView, UserlonginView

urlpatterns = [
        path('/user', UserSignUpView.as_view()),
        path('/login', UserlonginView.as_view())
    ]
