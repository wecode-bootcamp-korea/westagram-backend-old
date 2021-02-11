from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from .views import Register, LogIn

urlpatterns = [
    path('register/', Register.as_view()),
    path('login/', LogIn.as_view()),
]

