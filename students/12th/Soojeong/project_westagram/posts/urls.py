from django.urls import path
from .views import PostingView, PostDetailView

app_name="posts"

urlpatterns = [
        path('posting', PostingView.as_view()),
        path('postdetail', PostDetailView.as_view()),
]