
from django.urls import path
from posting.views import PostView, CommentView

urlpatterns = [
        path('/posting', PostView.as_view()),
        path('/posting/comment', CommentView.as_view())
        ]
