from django.urls import path

from posting.views import RegisterPost, ViewPost, DeletePost, UpdatePost, RegisterComment, ViewComment, DeleteComment, RegisterByComment, RegisterLikes, ViewLikes

urlpatterns = [
    path('register_post', RegisterPost.as_view()),
	path('view_post', ViewPost.as_view()),
    path('delete_post', DeletePost.as_view()),
    path('update_post', UpdatePost.as_view()),
    path('register_comment', RegisterComment.as_view()),
	path('view_comment', ViewComment.as_view()),
    path('delete_comment', DeleteComment.as_view()),
    path('register_bycomment', RegisterByComment.as_view()),
    path('register_likes', RegisterLikes.as_view()),
	path('view_likes', ViewLikes.as_view()),
]
