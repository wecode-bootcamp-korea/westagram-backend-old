from django.urls import path
from .views import PostingView, PostingSearchView

urlpatterns = [
    path('', PostingView.as_view()),
    path('/search', PostingSearchView.as_view()),
]
