from django.urls import path

from .views import ArticleView, CommentView

urlpatterns = [
    path('', ArticleView.as_view()),
    path('/comment', CommentView.as_view())
]
