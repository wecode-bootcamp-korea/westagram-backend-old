from django.urls import path
from .views      import PostView, CommentView, LikeView, DeletePostView, DeleteCommentView

urlpatterns = [
    path('' ,PostView.as_view()),
    path('like/<int:post_id>/', LikeView.as_view()),
    path('<int:post_id>/', CommentView.as_view()),
    path('post/<int:post_id>/', DeletePostView.as_view()),
    path('<int:post_id>/<int:comment_id>/', DeleteCommentView.as_view()),
]