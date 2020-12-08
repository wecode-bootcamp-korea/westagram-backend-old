from django.urls import path
from .views      import UserView

urlpatterns = [
    path('/sign-up', UserView.as_view()),
]
