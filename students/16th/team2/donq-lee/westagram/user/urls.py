from django.urls import path
from user.views import CreateUser

urlpatterns = [
    path('', CreateUser.as_view()),
]