from django.urls import path

from .views      import ArticleView, CommentView, LikeView

urlpatterns = [
    path('', ArticleView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/like', LikeView.as_view())
]
