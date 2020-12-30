from django.urls import path

from .views import (PostCreateView,
                    PostView, 
                    CommentCreateView, 
                    CommentView,
                    PostLikeView)

urlpatterns = [
    path("", PostView.as_view()),
    path("/create", PostCreateView.as_view()),
    path("/like", PostLikeView.as_view()),
    path("/<int:post_id>/comments", CommentView.as_view()),
    path("/<int:post_id>/comments/create", CommentCreateView.as_view()),
]
