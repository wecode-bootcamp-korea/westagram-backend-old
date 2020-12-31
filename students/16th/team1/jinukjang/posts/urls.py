from django.urls import path
from .views      import CreatePostView, ReadPostView, CreateCommentView, ReadCommentView

urlpatterns = [
    path('/createpost',CreatePostView.as_view()),
    path('/read',ReadPostView.as_view()),
    path('/comments/create',CreateCommentView.as_view()),
    path('/comments/read',ReadCommentView.as_view()),
]