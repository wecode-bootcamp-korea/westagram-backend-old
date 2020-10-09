from django.urls import path
from user.views  import RegisterView


urlpatterns = [
    path('', RegisterView.as_view())
]