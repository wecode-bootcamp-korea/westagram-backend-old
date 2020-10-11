from django.urls import path
from .views import PostingView,CommentView, LikeView

urlpatterns = [
    path('', PostingView.as_view()),
    path('create', PostingView.as_view()),
    path('<int:posting_id>/delete',PostingView.as_view()),
    path('<int:posting_id>/edit', PostingView.as_view()),
    # 댓글 확인
    path('<int:posting_id>/comments', CommentView.as_view()),
    # 댓글 달기
    path('<int:posting_id>/create', CommentView.as_view()),
    path('comments/delete', CommentView.as_view()),
    path('comments/edit', CommentView.as_view()),
    path('<int:posting_id>/like', LikeView.as_view()),
    
]