from django.urls import path

from post.views import PostView, CommentCreateView

urlpatterns=[
    path('', PostView.as_view()),
    path('/<int:post_id>/comments', CommentCreateView.as_view())
]

