from django.urls import path

from .views import SignUpView

app_name = 'account'

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name="sign-up"),
]