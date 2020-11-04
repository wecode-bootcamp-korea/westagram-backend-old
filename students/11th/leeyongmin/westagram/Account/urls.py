from django.urls import path
from . import views

app_name='Account'

urlpatterns = [
    path('signup', views.SignUp.as_view()),
    path('signin', views.SignIn.as_view()),
]