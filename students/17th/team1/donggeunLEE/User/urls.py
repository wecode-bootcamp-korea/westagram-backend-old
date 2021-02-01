from django.urls import path
from .views      import UserSignUpView

urlpatterns = [
        path('user', UserSignUpView.as_view())
    ]
