from django.urls import path
from .views      import PostingView

urlpatterns = [
    path('/posting', PostingView.as_view()),
]