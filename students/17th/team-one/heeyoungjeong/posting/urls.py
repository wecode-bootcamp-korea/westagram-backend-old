from django.urls import path
from posting.views import CommentView
from posting.views import PostingView


urlpatterns = [
    path('/comment', CommentView.as_view()),
    path('/create', PostingView.as_view()),
    path('', PostingView.as_view()),
]
