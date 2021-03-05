from django.urls import path, include
from .views import UploadView, ShowAllPostingView


urlpatterns = [
    path('/upload', UploadView.as_view()),
    path('/show-all', ShowAllPostingView.as_view())
]
