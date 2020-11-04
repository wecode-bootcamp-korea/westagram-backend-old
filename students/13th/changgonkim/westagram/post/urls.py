from django.urls import path
from post.views import PostView, ReadView, CommentView

urlpatterns = [
	path('/write'	, PostView.as_view()),
	path('/read'	, ReadView.as_view()),
	path('/comment'	, CommentView.as_view()),
]