from django.urls import path
from .views      import PostFeedView


urlpatterns = [
    path('', PostFeedView.as_view()),
]