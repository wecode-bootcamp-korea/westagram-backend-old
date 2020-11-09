from django.urls import path
from posting.views import PostingView

urlpatterns = [
    path('post', PostingView.as_view())
]
