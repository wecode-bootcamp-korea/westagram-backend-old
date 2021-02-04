from django.urls   import path

from posting.views import (
    PostView,
    PostShowView,
    CommentView,
    CommentShowView,
    PostLikeView
)

urlpatterns = [
    path('/post', PostView.as_view()),
    path('/postshow', PostShowView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/commentshow', CommentShowView.as_view()),
    path('/postlike', PostLikeView.as_view())
]
