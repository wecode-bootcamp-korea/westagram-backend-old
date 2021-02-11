from django.urls import path

from .views import PostView, CommentView, LikeView

urlpatterns = [
    path('', PostView.as_view()),
    path('cmt/', CommentView.as_view()),
    path('like/', LikeView.as_view()),
]
