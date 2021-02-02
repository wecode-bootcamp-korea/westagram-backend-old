from django.urls import path

from .views import (PostCreateView,
                    PostView, 
                    PostLikeView,
                    PostUpdateView,
                    PostDeleteView,
                    CommentCreateView, 
                    CommentView,
                    CommentDeleteView,
                    CommentAddComment)

urlpatterns = [
    path("", PostView.as_view()),
    path("/create", PostCreateView.as_view()),
    path("/delete", PostDeleteView.as_view()),
    path("/like", PostLikeView.as_view()),
    path("/<int:post_id>/update", PostUpdateView.as_view()),
    path("/<int:post_id>/comments", CommentView.as_view()),
    path("/<int:post_id>/comments/create", CommentCreateView.as_view()),
    path("/<int:post_id>/comments/<int:comment_id>/delete", CommentDeleteView.as_view()),
    path("/<int:post_id>/comments/<int:comment_id>/add-comment", CommentAddComment.as_view()),
]
