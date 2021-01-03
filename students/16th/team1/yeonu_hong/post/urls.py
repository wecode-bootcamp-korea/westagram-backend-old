from django.urls import path
from .views      import PostView, CommentView, LikeView

urlpatterns = [
    path('' ,PostView.as_view()),
    path('<int:post_id>/', CommentView.as_view()),
    path('<int:post_id>/<int:user_id>/', LikeView.as_view()),
]