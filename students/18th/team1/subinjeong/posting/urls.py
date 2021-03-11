from django.urls import path

from .views import PostingView


urlpatterns = [
    path('/posts',PostingView.as_view()),
    path('/upload',PostingView.as_view())
]