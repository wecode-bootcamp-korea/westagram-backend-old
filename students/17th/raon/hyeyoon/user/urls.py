from django.urls import path
from .views      import UserSignUpView

urlpatterns = [
    path('', UserSignUpView.as_view())
]
