from django.urls import path
from posting.views import PostingView, CommentView

urlpatterns = [
    path('/post', PostingView.as_view()),
    path('/comment', CommentView.as_view())
]
