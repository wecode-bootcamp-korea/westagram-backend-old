from django.urls import path
from user.views  import RegisterView, LoginView


urlpatterns = [
    path('', RegisterView.as_view()),
    path('/login', LoginView.as_view())
]