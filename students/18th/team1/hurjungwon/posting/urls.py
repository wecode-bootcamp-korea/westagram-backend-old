from django.urls import path

from posting.views import PostView, CommentView, LikeView, DeletePostView


urlpatterns = [
    path('/post', PostView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/like', LikeView.as_view()),
    path('/deletepost', DeletePostView.as_view())
]
