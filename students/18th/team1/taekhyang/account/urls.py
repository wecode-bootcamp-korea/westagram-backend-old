from django.urls import path, include

from .views import SignUpView


urlpatterns = [
    path('/sign-up', SignUpView.as_view())
]