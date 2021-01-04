from django.urls import path

from .views import (
    PostCreateView,
    PostReadView,
    PostDeleteView,
    PostUpdateView,
    CommentCreateView,
    CommentReadAllView,
    CommentReadView,
    CommentDeleteView,
    CommentUpdateView,
    LikeView,
)

urlpatterns = [
    path('/post_create',      PostCreateView.as_view()), 
    path('/post_read',        PostReadView.as_view()),
    path('/post_like',        LikeView.as_view()),
    path('/post_delete',      PostDeleteView.as_view()),
    path('/post_update',      PostUpdateView.as_view()),
    path('/comment_create',   CommentCreateView.as_view()),
    path('/comment_read_all', CommentReadAllView.as_view()),
    path('/comment_read',     CommentReadView.as_view()),
    path('/comment_delete',   CommentDeleteView.as_view()),
    path('/comment_update',   CommentUpdateView.as_view()),
]