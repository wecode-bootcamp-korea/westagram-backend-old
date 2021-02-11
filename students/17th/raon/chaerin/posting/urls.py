from django.urls      import path
from .views           import CommentView, PostView

urlpatterns = [
    path('/post', PostView.as_view()),
    path('/comment', CommentView.as_view())
    ]
