from django.urls import path
from post.views import (
    PostUp,
    PostList,
    PostListAll,
    AddComment,
    GetAllComments,
)

urlpatterns = [
    path('/postUp',         PostUp.as_view()),
    path('/postList',       PostList.as_view()),
    path('/postListAll',    PostListAll.as_view()),
    path('/comment/add',    AddComment.as_view()),
    path('/comment/getAll', GetAllComments.as_view()),
]