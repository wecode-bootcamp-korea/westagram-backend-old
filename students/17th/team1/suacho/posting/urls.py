from django.urls import path
from .views import (
    PostingView,
    PostingSearchView,
    PostingDetailView,
    CommentView,
    CommentDetailView,
    LikeView, 
)

urlpatterns = [
    path('', PostingView.as_view()),
    path('/<int:user_id>', PostingSearchView.as_view()),
    path('/<int:posting_id>', PostingDetailView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/comment/<int:posting_id>', CommentDetailView.as_view()),
    path('/like', LikeView.as_view()),
]
