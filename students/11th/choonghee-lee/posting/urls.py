from django.urls import path

from .views import PostView, CommentView

app_name = 'posting'

urlpatterns = [
    path('post/', PostView.as_view(), name="post"),
    path('comment/', CommentView.as_view(), name="create-comment"),
    path('comment/<int:post_id>', CommentView.as_view(), name="list-comment"),
]