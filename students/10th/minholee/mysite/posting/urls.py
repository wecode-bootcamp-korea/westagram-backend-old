from django.urls import path

from .views import PostView, CommentView


urlpatterns = [
    path('', PostView.as_view()),
    path('/comment', CommentView.as_view()),
]
