from django.urls import path

from .views import (PostView,CommentView)

app_name = 'post'

urlpatterns = [
    path('/', PostView.as_view()),
    path('/comment', CommentView.as_view(), name = 'comment'),
#    path('/like', LikeView.as_view(), name= 'like'),
]
