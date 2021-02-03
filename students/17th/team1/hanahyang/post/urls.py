from django.urls import path

from .views import PostView, CommentView, PostDetailView 

urlpatterns = [
    path('', PostView.as_view()),
    path('/comment', CommentView.as_view()),
    path('/<int:post_id>', PostDetailView.as_view()),
]
