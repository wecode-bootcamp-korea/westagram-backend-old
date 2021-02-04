from django.urls import path

from .views import PostView, CommentView, PostDetailView, LikeView 

urlpatterns = [
    path('', PostView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/<int:post_id>', PostDetailView.as_view()),
    path('/like', LikeView.as_view()),
]
