from django.urls import path

from .views import PostingView, GetPostView, CommentView, ShowCommentsView


urlpatterns = [
    path('/add', PostingView.as_view()),
    path('/list', GetPostView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/comment/<int:post_id>', ShowCommentsView.as_view())
]
