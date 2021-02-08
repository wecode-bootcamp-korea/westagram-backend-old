from django.urls import path

from .views import PostingView, CommentView, LikeView

urlpatterns = [
    path('', PostingView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/like', LikeView.as_view())
]
