from django.urls import path

from posting.views import (
        PostingView, GetArticlesView, ReplyCommentView, GetCommentsView,
        LikeView, GetLikesView
        )

urlpatterns = [
    path('/posting' , PostingView.as_view()),
    path('/articles', GetArticlesView.as_view()),
    path('/replying', ReplyCommentView.as_view()),
    path('/comments', GetCommentsView.as_view()),
    path('/liking',   LikeView.as_view()),
    path('/likes',    GetLikesView.as_view())
]
