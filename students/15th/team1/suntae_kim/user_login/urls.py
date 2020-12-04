from django.urls import path
from user_login.views import UserLogin

urlpatterns = [
 path('', UserLogin.as_view())
]
