from django.urls import path
from user.views import UsersView, LogInView

urlpatterns=[
    path('/create'  , UsersView.as_view()),
    path('/login'   , LogInView.as_view())
]