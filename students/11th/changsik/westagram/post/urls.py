from django.urls import path

from .views import PostView, CommentPostView, PostGetView, CommentGetView

urlpatterns = [
    path('post', PostView.as_view()),
    path('comment', CommentPostView.as_view()),
]
