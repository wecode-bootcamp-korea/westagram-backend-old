from django.urls import path
from .views import CommentView, PostingView, PostingSearchView

urlpatterns = [
    path('', PostingView.as_view()),
    path('/search', PostingSearchView.as_view()),
    path('/comment', CommentView.as_view()),
]
