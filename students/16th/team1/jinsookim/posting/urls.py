from django.urls import path
from posting.views import Post, Comment, Love_Function
urlpatterns = [
    path('/register', Post.as_view()),
    path('/comment', Comment.as_view()),
    path('/love', Love_Function.as_view())
]