from django.urls import path

from .views import PostsView, CommentCreateView, CommentListView

urlpatterns = [
    path('', PostsView.as_view(), name='post'),
    path('comment/', CommentCreateView.as_view(), name='comment'),
    path('<int:post_id>/comment/', CommentListView.as_view(), name='comment_list')
]
