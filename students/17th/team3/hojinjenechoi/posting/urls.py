from django.urls import path

from .views      import PostingView, CommentsView

urlpatterns = [
    path('/post', PostingView.as_view()), ## name?  ##as_view() is coming from View... inheritance. 
    path('/comment/<int:posting_id>', CommentsView.as_view())
]
