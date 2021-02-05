from django.urls import path
from .views import (
    PostingView, 
    PostingSearchView, 
    CommentView, 
    CommentDetailView, 
    LikeView, 
    LikeDetailView
)

urlpatterns = [
    path('', PostingView.as_view()),
    path('/search', PostingSearchView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/comment/<int:posting_id>', CommentDetailView.as_view()),
    path('/like', LikeView.as_view()),
    path('/like/<int:posting_id>', LikeDetailView.as_view()),
    ]
