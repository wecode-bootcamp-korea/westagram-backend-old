from django.urls import path

from posting.views import (
        PostingView, GetArticlesView, ReplyCommentView, GetCommentsView
        )

urlpatterns = [
    path('/posting' , PostingView.as_view()),
    path('/articles', GetArticlesView.as_view()),
    path('/replying', ReplyCommentView.as_view()),
    path('/comments', GetCommentsView.as_view())
]
