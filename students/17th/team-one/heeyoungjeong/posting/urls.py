from django.urls import path
from posting.views import PostingView

urlpatterns = [
    path('create', PostingView.as_view()),
    path('', PostingView.as_view()),
]
