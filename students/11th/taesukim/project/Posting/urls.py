from django.urls import path

from .views import PostView, GetView, CommentPost, CommentGet, LikePost, LikeGet

urlpatterns = [
    path('post', PostView.as_view()),
    path('get',  GetView.as_view()),
    path('commentpost', CommentPost.as_view()),
    path('commentget', CommentGet.as_view()),
    path('likepost', LikePost.as_view()),
    path('likeget', LikeGet.as_view()),
]
