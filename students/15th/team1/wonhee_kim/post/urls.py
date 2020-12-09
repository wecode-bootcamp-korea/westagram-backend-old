from django.urls import path

from .views import post_views, comment_views


urlpatterns = [
    path('/create/post', post_views.CreatePostView.as_view()),
    path('/read/post', post_views.ReadPostView.as_view()),
    path('/create/comment', comment_views.CreateCommentView.as_view()),
    path('/read/comment', comment_views.ReadCommentView.as_view()),
]