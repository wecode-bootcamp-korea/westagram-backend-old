from django.urls import path

from .views import (
    PostView, 
    PostDetailView, 
    CommentView, 
    CommentDetailView,
    LikeView, 
)

urlpatterns = [
    path('', PostView.as_view()),
    path('/<int:post_id>', PostDetailView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/comment/<int:comment_id>', CommentDetailView.as_view()),
    path('/like', LikeView.as_view()),
]
