from django.urls import path

from posting.views import PostUploadView, CommentUploadView

urlpatterns = [
    path('/post', PostUploadView.as_view()),
    path('/comment', CommentUploadView.as_view())
]