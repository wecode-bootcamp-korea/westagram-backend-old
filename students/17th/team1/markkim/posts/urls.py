from django.urls import path
from . views     import PostView, CommentView, CommentDetailView, PostDetailView, LikeView, LikeDetailView


urlpatterns = [
        path('', PostView.as_view()),
        path('/<int:post_id>', PostDetailView.as_view()),
        path('/comment', CommentView.as_view()),
        path('/comment/<int:post_id>', CommentDetailView.as_view()),
        path('/like', LikeView.as_view()),
        path('/like/<int:post_id>', LikeDetailView.as_view())
        ]
