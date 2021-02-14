from django.urls   import path

from posting.views import (
    PostView,
    PostShowView,
    CommentView,
    CommentShowView,
    PostLikeView, 
    FollowView,
    CommentDeleteView,
    PostDeleteView,
    PostModifyView,
    FollowShowView,
)

urlpatterns = [
    path('/post', PostView.as_view()),
    path('/postshow', PostShowView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/commentshow', CommentShowView.as_view()),
    path('/postlike', PostLikeView.as_view()),
    path('/follow', FollowView.as_view()),
    path('/commentdelete', CommentDeleteView.as_view()),
    path('/postdelete', PostDeleteView.as_view()),
    path('/postmodify', PostModifyView.as_view()),
    path('/followshow', FollowShowView.as_view()),
]
