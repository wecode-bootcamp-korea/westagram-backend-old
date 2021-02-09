

from django.urls import path
from posting.views import PostingView, CommentView, LikeView

urlpatterns = [
        path('post', PostingView.as_view()),
        path('comment', CommentView.as_view()),
        path('like', LikeView.as_view()),
]
