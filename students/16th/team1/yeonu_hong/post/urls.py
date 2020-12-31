from django.urls import path
from .views      import PostView, CommentView

urlpatterns = [
    path('' ,PostView.as_view()),
    path('<int:post_id>/', CommentView.as_view()),
]