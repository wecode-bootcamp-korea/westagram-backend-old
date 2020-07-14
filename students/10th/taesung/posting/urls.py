from django.urls import path

from .views import ArticleView, Comment

urlpatterns = [
    path('', ArticleView.as_view()),
    path('/comment_log', Comment.as_view())
]
