from django.urls import  path
from .views import UsersView, LoginView

urlpatterns = [
    path('/register', UsersView.as_view()),
    path('/login', LoginView.as_view()),
]
