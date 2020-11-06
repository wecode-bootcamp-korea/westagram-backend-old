from django.urls import path
from .views import UserView, LogInView

urlpatterns = [
    path('', UserView.as_view()),
    path('/login',LogInView.as_view())
]
