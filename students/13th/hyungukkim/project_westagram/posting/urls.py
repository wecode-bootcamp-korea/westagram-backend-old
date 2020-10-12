from django.urls import path
from posting.views import RegisterPost, ViewPost

urlpatterns = [
    path('register_post', RegisterPost.as_view()),
	path('view_post', ViewPost.as_view())
]
