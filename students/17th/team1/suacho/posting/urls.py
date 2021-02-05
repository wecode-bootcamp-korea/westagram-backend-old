from django.urls import path
from .views import CommentView, LikeView, PostingView, PostingSearchView

urlpatterns = [
    path('', PostingView.as_view()),
    path('/search', PostingSearchView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/like', LikeView.as_view()),
]
