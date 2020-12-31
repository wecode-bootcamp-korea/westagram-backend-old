from django.urls import path
from user.views import Sign_Up, Sign_in
urlpatterns = [
    path('/sign_up', Sign_Up.as_view()),
    path('/sign_in', Sign_in.as_view())
]