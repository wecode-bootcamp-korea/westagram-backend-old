from django.urls import path
from .views import PostingView, CommentView

urlpatterns = [
    path('/create', PostingView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/retrieve', PostingView.as_view()),
]
