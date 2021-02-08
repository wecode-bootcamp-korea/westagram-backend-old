from django.urls import path
from posting.views  import (
                           PostingView, 
                           PostingDetailView, 
                           CommentView,
                           LikeView
)

urlpatterns = [
    path('', PostingView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/like', LikeView.as_view())
   # path('/<drink/<int:posting_id>', PostingDetailView.as_view())
]