from django.urls import path

from .views import SignupView, LoginView

urlpatterns = [
    path('user', SignupView.as_view()),
    path('login', LoginView.as_view()),
]
