from django.urls import path

from .views.post_views        import PostView, LoadAllPostView
from .views.comment_views     import CommentView
from .views.like_views        import LikeView


urlpatterns = [
    path('', LoadAllPostView.as_view()),
    path('/post', PostView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/like', LikeView.as_view()),
]






