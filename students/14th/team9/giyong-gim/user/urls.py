from django.urls import path

from django.conf import settings

from .views import Register, LogIn, ProfileView

app_name='user'

urlpatterns = [
    path('register', Register.as_view(), name = 'register'),
    path('login', LogIn.as_view(), name = 'login'),
    path('<str:username>', ProfileView.as_view(), name = 'profile'),
]

