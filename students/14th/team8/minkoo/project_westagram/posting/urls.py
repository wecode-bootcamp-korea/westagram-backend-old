from django.urls import path

from .views import PostsView, CommentCreateView, CommentListView, LikeView, LikeListView

urlpatterns = [
    path('', PostsView.as_view(), name='post'),
    path('comment/', CommentCreateView.as_view(), name='comment'),
    path('<int:post_id>/comment/', CommentListView.as_view(), name='comment_list'),
    path('like/', LikeView.as_view(), name='like'),
    path('<int:user_id>/like/list/', LikeListView.as_view(), name='like_list')
]
