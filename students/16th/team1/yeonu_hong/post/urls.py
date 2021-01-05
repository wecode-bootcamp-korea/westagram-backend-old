from django.urls import path
from .views      import PostView, CommentView, LikeView, PostDeleteView, CommentDeleteView, PostUpdateView

urlpatterns = [
    path('' ,PostView.as_view()),
    path('like/<int:post_id>/', LikeView.as_view()),
    path('<int:post_id>/', CommentView.as_view()),
    path('post/<int:post_id>/', PostDeleteView.as_view()),
    path('update/<int:post_id>/', PostUpdateView.as_view()),
    path('<int:post_id>/<int:comment_id>/', CommentDeleteView.as_view()),

]