from django.urls import path
from user.views import SignInView

urlpatterns = [
    path('/signin', SignInView.as_view())
]