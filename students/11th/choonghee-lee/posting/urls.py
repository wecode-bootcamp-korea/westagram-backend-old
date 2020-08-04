from django.urls import path

from .views import (
    CreatePostView, 
    ListPostView,
    CreateCommentView,
    ListCommentView
)

app_name = 'posting'

urlpatterns = [
    path('create-post/', CreatePostView.as_view(), name="create-post"),
    path('list-post/', ListPostView.as_view(), name="list-post"),
    path('create-comment/', CreateCommentView.as_view(), name="create-comment"),
    path(
        'list-comment/<int:post_id>',
        ListCommentView.as_view(),
        name="list-comment",
    ),
]