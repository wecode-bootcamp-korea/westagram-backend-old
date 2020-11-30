from django.urls    import path

from .views         import PostingView, ReadPostingView, CreateCommentingView, ReadCommentingView

urlpatterns = [
    path('/create', PostingView.as_view()),
    path('/read',   ReadPostingView.as_view()),
    path('/create/comment', CreateCommentingView.as_view()),
    path('/read/comment', ReadCommentingView.as_view())
]
