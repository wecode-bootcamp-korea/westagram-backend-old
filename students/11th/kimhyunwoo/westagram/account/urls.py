from django.urls import path
from .views import SignUpView, SignInView

urlpatterns = [
    path('sign_up',SignUpView.as_view()),
    path('sign_in',SignInView.as_view())
 ]