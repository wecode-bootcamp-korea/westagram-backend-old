from django.urls import path
from .views import PostingView, CommentView, LikeView, ReplyView

urlpatterns = [
    path('/create', PostingView.as_view()),
    path('/update', PostingView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/comment/delete', CommentView.as_view()),
    path('/reply', ReplyView.as_view()),
    path('/retrieve', PostingView.as_view()),
    path('/delete', PostingView.as_view()),
    path('/like', LikeView.as_view()),
]
