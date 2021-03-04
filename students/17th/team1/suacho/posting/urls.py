from django.urls import path
from .views import (
    PostingView,
    PostingSearchView,
    PostingDetailView,
    CommentView,
    CommentSearchView,
    CommentDetailView,
    LikeView, 
)

urlpatterns = [
    path('', PostingView.as_view()),
    path('/search/<int:user_id>', PostingSearchView.as_view()),
    path('/<int:posting_id>', PostingDetailView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/comment/search/<int:posting_id>', CommentSearchView.as_view()),
    path('/comment/<int:comment_id>', CommentDetailView.as_view()),
    path('/like', LikeView.as_view()),
]
