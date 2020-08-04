from django.urls import path

from .views import SignupView

urlpatterns = [
    path('user', SignupView.as_view()),
]
