from django.urls import path

from .views import UserSignUp

urlpatterns = [
   path('', UserSignUp.as_view()),
]
