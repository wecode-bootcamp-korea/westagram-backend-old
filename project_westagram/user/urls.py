from django.urls import path
from user.views  import SignUp, LoginView

app_name = 'user'

urlpatterns = [
    path('', SignUp.as_view()),
    path('/login', LoginView.as_view()),
]
