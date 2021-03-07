from django.urls import path, include
from .views import PostingUploadView, ShowAllPostingView, CommentRegisterView, ShowCommentView, PostingLikeView, ShowPostingLikeCountView


urlpatterns = [
    path('/upload', PostingUploadView.as_view()),
    path('/show-all', ShowAllPostingView.as_view()),
    path('/comment', CommentRegisterView.as_view()),
    path('/comment/show', ShowCommentView.as_view()),
    path('/like', PostingLikeView.as_view()),
    path('/like/show', ShowPostingLikeCountView.as_view())
]
