from django.urls import path
from posting.views import CommentView
from posting.views import CommentDeleteView
from posting.views import CommentDetailView
from posting.views import LikeView
from posting.views import PostingView
from posting.views import PostingDeleteView
from posting.views import UnlikeView


urlpatterns = [
    path('/comment', CommentView.as_view()),
    path('/comment/<int:posting_id>', CommentDetailView.as_view()),
    path('/create', PostingView.as_view()),
    path('/comment/<int:comment_id>/delete', CommentDeleteView.as_view()),
    path('/<int:posting_id>/delete', PostingDeleteView.as_view()),
    path('/<int:posting_id>/like', LikeView.as_view()),
    path('/<int:posting_id>/unlike', UnlikeView.as_view()),
    path('', PostingView.as_view()),
]
