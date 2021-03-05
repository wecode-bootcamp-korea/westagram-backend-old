from django.urls import path
from .views      import PostingView, ShowView

urlpatterns = [
    path('/posting', PostingView.as_view()),
    path('/show', ShowView.as_view()),    
]