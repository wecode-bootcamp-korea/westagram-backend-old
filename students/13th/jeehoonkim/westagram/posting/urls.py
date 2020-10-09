from django.urls import path
from .views import PostingView,CommentView

urlpatterns = [
    path('', PostingView.as_view()),
    path('create', PostingView.as_view()),
    path('<int:posting_id>/create', CommentView.as_view()),
]