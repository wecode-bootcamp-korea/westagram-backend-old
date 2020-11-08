from django.urls import path

from .views import PostsView, PostDetailView, CommentView, CommentListView, LikeView, LikeListView

urlpatterns = [
    path('', PostsView.as_view(), name='post'),
    path('<int:post_id>', PostDetailView.as_view(), name='post_detail'),
    path('comment/', CommentView.as_view(), name='comment'),
    path('<int:post_id>/comment/', CommentListView.as_view(), name='comment_list'),
    path('like/', LikeView.as_view(), name='like'),
    path('like/list/<int:user_id>', LikeListView.as_view(), name='like_list'),
]
