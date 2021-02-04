from django.urls   import path

from posting.views import PostView, PostShowView, CommentView

urlpatterns = [
    path('/post', PostView.as_view()),
    path('/postshow', PostShowView.as_view()),
    path('/comment', CommentView.as_view()),
    # path('/commentshow', PostShowView.as_view()),
]
