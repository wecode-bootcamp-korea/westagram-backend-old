from django.urls import path
from .views      import PostingView, ShowView, CommentView

urlpatterns = [
    path('/posting', PostingView.as_view()),
    path('/show', ShowView.as_view()),    
    path('/comment', CommentView.as_view()),        
]