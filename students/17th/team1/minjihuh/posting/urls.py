from django.urls import path
from posting.views  import PostingView, PostingDetailView

urlpatterns = [
    path('', PostingView.as_view()),
    path('/<drink/<int:posting_id>', PostingDetailView.as_view())
]