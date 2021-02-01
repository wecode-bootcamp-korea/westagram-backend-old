from django.urls import path

from user.views import AccountView, LoginView
urlpatterns = [
    path('', AccountView.as_view()),
    path('/login', LoginView.as_view())
]