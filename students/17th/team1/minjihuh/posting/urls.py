from django.urls import path
from posting.views  import (
                           PostingView, 
                           PostingDetailView, 
                           CommentView,
                           CommentDetailView,
                           LikeView
)

urlpatterns = [
    path('', PostingView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/like', LikeView.as_view()),
    path('/comment/<int:comment_id>', CommentDetailView.as_view()),
    path('/<int:posting_id>', PostingDetailView.as_view())
]