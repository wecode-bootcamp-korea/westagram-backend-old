from django.urls import path

from . import views

urlpatterns = [
    path("comment", views.CommentView.as_view()),
    path("posting", views.PostingView.as_view()),
    path("love", views.LoveView.as_view()),
]
