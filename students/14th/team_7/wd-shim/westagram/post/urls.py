from django.urls import path
from post.views import PostUp, PostList, PostListAll

urlpatterns = [
    path('/p', PostUp.as_view()),
    path('/p/list', PostList.as_view()),
    path('/p/all', PostListAll.as_view()),
]