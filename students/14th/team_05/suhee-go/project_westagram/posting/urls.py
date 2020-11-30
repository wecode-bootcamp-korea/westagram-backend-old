from django.urls import path
from .views      import CreatePostView, ReadPostView, CreateCommentView, ReadCommentView

urlpatterns= [
    path('create', CreatePostView.as_view()),
    path('read', ReadPostView.as_view()),
    path('create/comment', CreateCommentView.as_view()),
    path('read/comment', ReadCommentView.as_view())
]
