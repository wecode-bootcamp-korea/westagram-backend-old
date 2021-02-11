from django.urls import path
from user.views  import (
    RegisterView, 
    LoginView, 
    FollowView
)

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('follow/<int:user_id>', FollowView.as_view())
]