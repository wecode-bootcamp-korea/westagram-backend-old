from django.urls  import path
from .views       import Post, CommentView

urlpatterns = [
    path('post', Post.as_view()),
    path('comment', CommentView.as_view())
]