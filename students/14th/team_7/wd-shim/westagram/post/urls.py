from django.urls import path
from post.views import (
    PostUp,
    PostList,
    PostListAll,
    AddComment,
    GetComments,
)

urlpatterns = [
    path('/postUp',      PostUp.as_view()),
    path('/postList',    PostList.as_view()),
    path('/postListAll', PostListAll.as_view()),
    path('/addComment',  AddComment.as_view()),
    path('/getComments', GetComments.as_view()),
]