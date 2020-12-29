from django.urls import path

from .views import PostCreateView, PostView

urlpatterns = [
    path("", PostView.as_view()),
    path("/create", PostCreateView.as_view())
]
