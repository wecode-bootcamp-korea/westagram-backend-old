from django.urls import path

from .views      import PostView, CommentsView, LikeView

urlpatterns = [
    path('', PostView.as_view()),
    path('/comment', CommentsView.as_view()),
    path('/like', LikeView.as_view()),
]

