from django.urls import path

from user.views import SignUpView

urlpatterns = [
    path('', SignUpView.as_view())
]