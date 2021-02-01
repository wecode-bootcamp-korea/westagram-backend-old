

from django.urls import path
from users.views import SignUp, Login

urlpatterns = [
        path('signup', SignUp.as_view()),
        path('login', Login.as_view())
]
