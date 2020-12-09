from django.urls import path

from .views.post_views        import CreatePostView, ReadPostView, ReadPostDetailView
from .views.comment_views     import CreateCommentView, ReadCommentView
from .views.like_views        import LikeView


urlpatterns = [
    # base
    path('', ReadPostView.as_view()),
    path('/<int:post_id>', ReadPostDetailView.as_view()),
    path('/post/create', CreatePostView.as_view()),

    # comment
    path('/comment/create/<int:post_id>', CreateCommentView.as_view()),
    path('/comment/read/<int:post_id>', ReadCommentView.as_view()),

    # like
    path('/like/<int:post_id>', LikeView.as_view()),
]






