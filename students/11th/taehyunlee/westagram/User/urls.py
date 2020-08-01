from django.urls import path

from . import views

urlpatterns = [
    path('', views.SignUp.as_view()),
]
