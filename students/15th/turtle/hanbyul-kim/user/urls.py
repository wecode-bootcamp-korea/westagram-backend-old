from django.urls import path
from user.views import UserView

urlpatterns = [
    path('/sign-up',UserView.as_view(), name ='sign-up'),
]
