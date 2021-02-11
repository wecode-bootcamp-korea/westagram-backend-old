from django.urls import path
from board.views import BoardView,CommentView

urlpatterns = [
        path('', BoardView.as_view()),
        path('comment', CommentView.as_view()), 
]
