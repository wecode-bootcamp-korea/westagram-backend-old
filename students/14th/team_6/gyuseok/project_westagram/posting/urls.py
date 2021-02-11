from django.urls import path
from .views import BoardView, CommentView, LikeView

urlpatterns = [
    path('/board',BoardView.as_view()),
    path('/comment',CommentView.as_view()),
    path('/like',LikeView.as_view()),
]
