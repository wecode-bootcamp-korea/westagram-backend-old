from django.urls import path

from .views import (PostView, CommentView, LikeView, FollowView, PostDetailVeiw)

app_name = 'post'

urlpatterns = [
    path('/', PostView.as_view()),
    path('/comment', CommentView.as_view(), name='comment'),
    path('/like', LikeView.as_view(), name='like'),
    path('/follow', FollowView.as_view(), name='follow'),
    path('/<str:username>', PostDetailVeiw.as_view(), name='detail'),
]
