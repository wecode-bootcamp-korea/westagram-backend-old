from django.urls import path
from .views      import (PostView,
        PostDetailView,
        CommentView,
        CommentDetailView,
        AddCommentView,
        LikeView
        )

urlpatterns = [
       path('', PostView.as_view()),
       path('/postdetail/<int : post_id>', PostDetailView.as_view()),
       path('/comment', CommentView.as_view()),
       path('/commentdetail/<int : comment_id>', CommentDetailView.as_view()),
       path('/add', AddCommentView.as_view()),
       path('/like', LikeView.as_view())
    ]
