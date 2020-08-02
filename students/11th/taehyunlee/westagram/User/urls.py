from django.urls import path

from . import views

urlpatterns = [
    path('SignUp', views.SignUp.as_view()),
    path('SignIn', views.SignIn.as_view()),
]
