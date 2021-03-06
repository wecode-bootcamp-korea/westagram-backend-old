from django.urls import path

from .views import PostingView, GetPostView


urlpatterns = [
    path('/add', PostingView.as_view()),
    path('/list', GetPostView.as_view())
]
