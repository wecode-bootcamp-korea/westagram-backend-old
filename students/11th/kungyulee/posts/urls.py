from django.urls import path

from .views import PostView, CommentView, PostDetailView, GetToken

urlpatterns = [
    path('posting', PostView.as_view()),
    path('comment', CommentView.as_view()),
    path('posting/<int:pk>', PostDetailView.as_view()),
    path('token', GetToken.as_view()),
]
