from django.urls import path
from .views import CreateBoardView, ReadBoardView, CreateCommentView

urlpatterns = [
    path('register/',CreateBoardView.as_view()),
    path('express/',ReadBoardView.as_view()),
    path('comment/create/',CreateCommentView.as_view()),
]
