from django.urls import path
from .views      import ContentView, CommentView

urlpatterns = [
    path('/posting', ContentView.as_view()),
    path('/comment', CommentView.as_view())
]