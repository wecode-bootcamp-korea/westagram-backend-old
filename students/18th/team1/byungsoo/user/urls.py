from django.urls import path

from .views import SignUpView

urlpatterns = [
   path('/users', SignUpView.as_view()),
]
