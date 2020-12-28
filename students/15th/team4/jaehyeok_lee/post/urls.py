from django.urls import path

from . import views

urlpatterns = [
    path('posting', views.PostingView.as_view()),
    path('comment', views.CommentView.as_view()),
]
