from django.urls import path
from .views      import PostFeedView


urlpatterns = [
    path('/posting', PostFeedView.as_view()),
]