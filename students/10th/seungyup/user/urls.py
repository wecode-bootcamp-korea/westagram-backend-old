from django.urls import path

from .views import SignInView, SignUpView

urlpatterns =[
    path('', SignUpView.as_view()),
    path('/sign-in', SignInView.as_view())
]
