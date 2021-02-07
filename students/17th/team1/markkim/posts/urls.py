from django.urls import path
from . views     import PostView, CommentView, CommentDetailView


urlpatterns = [
        path('', PostView.as_view()),
        path('/comment', CommentView.as_view()),
        path('/comment/<int:post_id>', CommentDetailView.as_view()),
        ]
