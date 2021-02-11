from django.urls import  path
from .views import UsersView, LoginView, FollowView

urlpatterns = [
    path('/register', UsersView.as_view()),
    path('/login', LoginView.as_view()),
    path('/follow', FollowView.as_view()),
]
