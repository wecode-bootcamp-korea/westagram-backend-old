from django.urls import path
from .views import (
                RegistView
                , LoginView
                )

urlpatterns=[
        path('regist', RegistView.as_view()),
        path('login', LoginView.as_view()),
        ]
