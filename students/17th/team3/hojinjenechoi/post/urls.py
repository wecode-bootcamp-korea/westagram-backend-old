from django.urls import path

from .views      import PostView, CommentsView, LikeView

urlpatterns = [
    path('', PostView.as_view()),
    path('/comment/<int:post_id>', CommentsView.as_view()),
    path('/like/<int:post_id>', LikeView.as_view()),
]

