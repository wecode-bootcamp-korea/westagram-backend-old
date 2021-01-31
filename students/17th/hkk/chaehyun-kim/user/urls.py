from django.urls import path, include

from .views import UserView

urlpatterns = [
    path('/signup', UserView.as_view())
]
