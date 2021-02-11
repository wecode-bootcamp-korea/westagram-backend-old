from django.urls import path

from .views import (
    PostView, 
    PostDisplayView,
    CommentView,
    CommentDisplayView
)

urlpatterns = [
    path('post', PostView.as_view()),
    path('postdisplay', PostDisplayView.as_view()),
    path('comment', CommentView.as_view()),
    path('commentdisplay/<int:post_id>', CommentDisplayView.as_view())
]
