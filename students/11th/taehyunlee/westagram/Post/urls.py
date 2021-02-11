from django.urls import path

from .views import PostingView, CommentView

urlpatterns = [
    path('posting', PostingView.as_view()),
    path('comment', CommentView.as_view()),
]