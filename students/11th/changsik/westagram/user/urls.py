from django.urls import path

from .views import SignUpView

urlpatterns = [
    path('Users', SignUpView.as_view())
]