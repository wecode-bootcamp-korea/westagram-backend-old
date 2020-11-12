from django.urls import path
from .views import BoardView, CommentView

urlpatterns = [
    path('/board',BoardView.as_view()),
    path('/comment',CommentView.as_view()),
]
