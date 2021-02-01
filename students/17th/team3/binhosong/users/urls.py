

from django.urls import path
from users.views import SignUp

urlpatterns = [
        path('', SignUp.as_view())
]
