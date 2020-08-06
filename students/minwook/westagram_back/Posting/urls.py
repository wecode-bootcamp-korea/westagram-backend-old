from django.urls import path

from . views import PostView, CommentView

urlpatterns = [
    path('Post', PostView.as_view()),
    path('Comment', CommentView.as_view())
]
