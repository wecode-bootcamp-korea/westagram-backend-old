from django.urls import path, include
from .views      import (
    PostView, PostGet,
    CommentPost, CommentView
)

urlpatterns = [
    path('post_view', PostView.as_view()),
    path('post_get', PostGet.as_view()),
    path('post_comment', CommentPost.as_view()),
    path('view_comment', CommentView.as_view())
]