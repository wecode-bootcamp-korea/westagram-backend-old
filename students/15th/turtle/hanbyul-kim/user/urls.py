from django.urls import path
from user.views import UserView, SigninView

urlpatterns = [
    path('/sign-up',UserView.as_view(), name ='sign-up'),
    path('/sign-in',UserView.as_view(), name ='sign-in'),
]
