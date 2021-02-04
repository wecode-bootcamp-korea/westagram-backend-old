from django.urls import path

from posting.views import PostView, ShowView

urlpatterns = [
    path('/post', PostView.as_view()),
    path('/show', ShowView.as_view()),
]
