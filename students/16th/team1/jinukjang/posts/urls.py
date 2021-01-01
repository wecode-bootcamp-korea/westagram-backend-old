from django.urls import path
from .views      import CreatePostView, PostView, CreateCommentView, CommentView, PostLikeView

urlpatterns = [
    path('',PostView.as_view()),
    path('/create',CreatePostView.as_view()),
    path('/comments',CommentView.as_view()),
    path('/comments/create',CreateCommentView.as_view()),
    path('/like',PostLikeView.as_view()),
]