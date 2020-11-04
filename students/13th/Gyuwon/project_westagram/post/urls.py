from django.urls import path
from post.views import PostView, CommentView

urlpatterns = [
    path('post', PostView.as_view()),
    path('comment', CommentView.as_view())
]