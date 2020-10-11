from django.urls   import path
from posting.views import (
    CreatePost, 
    PostView, 
    CreateComment,
    CommentView
)

urlpatterns = [
    path('<int:user_id>'       , PostView.as_view()),
    path('create' , CreatePost.as_view()),
    path('<int:post_id>/comment/create', CreateComment.as_view()),
    path('<int:post_id>/comment', CommentView.as_view())
]