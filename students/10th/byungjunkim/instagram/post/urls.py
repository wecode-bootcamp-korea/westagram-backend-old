
from django.urls import path

from .views import PostView,CommentView,ThumbsView

urlpatterns = [
    path('/',PostView.as_view()),
    path('/comment',CommentView.as_view()),
    path('/thumbs',ThumbsView.as_view())
]
