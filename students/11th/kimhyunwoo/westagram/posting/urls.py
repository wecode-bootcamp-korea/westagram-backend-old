from django.urls import path
from .views import PostingView
from .views import CommentView
urlpatterns = [
    path('post',PostingView.as_view()),
    path('comment',CommentView.as_view())
 ]