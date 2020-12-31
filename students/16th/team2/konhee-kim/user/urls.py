from django.urls import path
from user.views import SignUpView

urlpatterns = [
    path('/sign-up', SignUpView.as_view())
]
