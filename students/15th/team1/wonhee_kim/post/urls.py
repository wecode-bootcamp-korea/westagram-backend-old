from django.urls import path

from .views.post_views        import CreatePostView, ReadPostView, ReadPostDetailView, DeletePostView
from .views.comment_views     import CreateCommentView, ReadCommentView, DeleteCommentView
from .views.like_views        import LikeView


urlpatterns = [
    # base
    path('', ReadPostView.as_view()),

    # post
    path('/<int:post_id>', ReadPostDetailView.as_view()),
    path('/post/create', CreatePostView.as_view()),
    path('/post/delete/<int:post_id>', DeletePostView.as_view()),

    # comment
    path('/comment/create/<int:post_id>', CreateCommentView.as_view()),
    path('/comment/read/<int:post_id>', ReadCommentView.as_view()),
    path('/comment/delete/<int:comment_id>', DeleteCommentView.as_view()),

    # like
    path('/like/<int:post_id>', LikeView.as_view()),
]






