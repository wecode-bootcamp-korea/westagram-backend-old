from django.urls import path

from user.views import AccountView, LoginView, FollowView
urlpatterns = [
    path('', AccountView.as_view()),
    path('/login', LoginView.as_view()),
    path('/follow', FollowView.as_view())
]