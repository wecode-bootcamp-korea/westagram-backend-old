from django.urls import path

from account.views import SignUpView

urlpatterns = [
  path('/signup', SignUpView.as_view())
]
