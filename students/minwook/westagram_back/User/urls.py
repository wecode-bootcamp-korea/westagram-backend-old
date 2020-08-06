from django.urls import path
from .views import SignUpView, SignInView

urlpatterns = [
    path('SignUp', SignUpView.as_view()),
    path('SignIn', SignInView.as_view())
]
