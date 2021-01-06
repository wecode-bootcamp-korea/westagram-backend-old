from django.urls import path
from .views      import (
    CreatePostView,
    PostView,
    CreateCommentView,
    CommentView, 
    LikePostView,
    DeletePostView,
    DeleteCommentView,
    EditPostView
)

urlpatterns = [
    path('',                 PostView.as_view()),
    path('/create',          CreatePostView.as_view()),
    path('/edit',            EditPostView.as_view()),
    path('/delete',          DeletePostView.as_view()),
    path('/like',            LikePostView.as_view()),
    path('/comments',        CommentView.as_view()),
    path('/comments/create', CreateCommentView.as_view()),
    path('/comments/delete', DeleteCommentView.as_view()),
]