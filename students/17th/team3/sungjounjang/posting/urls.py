from django.urls import path

from .views import PostingView, CommentView, LikePostingView

urlpatterns = [
    path('', PostingView.as_view()),
    path('/<str:account>/<int:posting>', PostingView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/comment/<str:account>/<int:posting>/<int:comment>', CommentView.as_view()),
    path('/like/post', LikePostingView.as_view()),
]