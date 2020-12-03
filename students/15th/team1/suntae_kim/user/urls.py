from django.urls import path
from user.views import UserView

urlpatterns = [
    path('', UserView.as_view())
]
