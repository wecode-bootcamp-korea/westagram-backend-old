from django.urls import path

from .views import UserRegisterView

app_name = "account"

urlpatterns = [
    path('', UserRegisterView.as_view(), name="user_register"),
]