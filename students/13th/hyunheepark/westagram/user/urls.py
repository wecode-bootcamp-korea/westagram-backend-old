from django.urls import path
from user.views  import SignUpView,SignInView
from . import views

urlpatterns = [
        path('',views.IndexView),
        path('/up',SignUpView.as_view()),
        path('/in',SignInView.as_view())
        ]
