from django.urls import path

from .views import (
    PostCreateView,
    PostReadView,
    CommentCreateView,
    CommentReadAllView,
    CommentReadView,
    LikeView,
)

urlpatterns = [
    path('/post_create', PostCreateView.as_view()), 
    path('/post_read', PostReadView.as_view()),
    path('/post_like', LikeView.as_view()),
    path('/comment_create', CommentCreateView.as_view()),
    path('/comment_read_all',CommentReadAllView.as_view()),
    path('/comment_read',CommentReadView.as_view()),
]