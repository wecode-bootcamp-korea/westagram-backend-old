from django.urls import path
from .views      import PostView, CommentView, ListCommentView

urlpatterns = [
    path('post', PostView.as_view()),
    path('comment', CommentView.as_view()),
    path('list/<int:post_id>', ListCommentView.as_view()),
]
