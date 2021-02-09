from django.urls import path

from .views import PostingView, PostingDetailView, CommentView, CommentDetailView, LikeView, LikeDetailView

urlpatterns = [
    path('', PostingView.as_view()),
    path('/<int:user_id>', PostingDetailView.as_view()),
    path('/<int:posting_id>', PostingDetailView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/comment/postingnum/<int:posting_id>', CommentDetailView.as_view()),
    path('/comment/<int:comment_id>', CommentDetailView.as_view()),
    path('/like', LikeView.as_view()),
    path('/like/<int:posting_id>', LikeDetailView.as_view()),
]
