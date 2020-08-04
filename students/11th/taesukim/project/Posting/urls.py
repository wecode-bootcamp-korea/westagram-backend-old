from django.urls import path

from .views import PostView, GetView, CommentPost, CommentGet

urlpatterns = [
    path('post', PostView.as_view()),
    path('get',  GetView.as_view()),
    path('commentpost', CommentPost.as_view()),
    path('commentget', CommentGet.as_view()),
]
