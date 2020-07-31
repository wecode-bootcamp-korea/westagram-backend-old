from django.urls import path

from . import views

urlpatterns = [
    path("", views.UserView.as_view()),
    path("login", views.LoginView.as_view()),
    path("follow", views.FollowView.as_view()),
]
