from django.urls import path
from .views      import PostUpView


urlpatterns = [
    path('/postup', PostUpView.as_view()),
]