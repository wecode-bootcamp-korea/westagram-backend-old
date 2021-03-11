from django.urls import path, include
from .views import SignUpView, LoginView, ShowRecommendedUser


urlpatterns = [
    path('/sign-up', SignUpView.as_view()),
    path('/login', LoginView.as_view()),
    path('/recommended', ShowRecommendedUser.as_view())
]
