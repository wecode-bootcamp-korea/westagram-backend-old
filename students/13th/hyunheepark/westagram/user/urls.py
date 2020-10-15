from django.urls import path
from user.views  import SignUpView,SignInView 
from . import views

urlpatterns = [
        path('',views.IndexView),
        path('/signup',SignUpView.as_view()),
        path('/signin',SignInView.as_view()),
                ]
