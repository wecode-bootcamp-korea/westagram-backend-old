from django.urls import path, include
from .views import PostingUploadView, ShowAllPostingView, CommentRegisterView, ShowCommentView


urlpatterns = [
    path('/upload', PostingUploadView.as_view()),
    path('/show-all', ShowAllPostingView.as_view()),
    path('/comment', CommentRegisterView.as_view()),
    path('/show-comment', ShowCommentView.as_view())
]
