from django.urls import path
from .views import signUp, signIn

urlpatterns = [
        path('', signUp.as_view()),
        path('log/', signIn.as_view())
        ]
