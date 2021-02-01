from django.urls import path
from user.views import SignUp

urlpatterns = [
    path('', SignUp.as_view())
]

