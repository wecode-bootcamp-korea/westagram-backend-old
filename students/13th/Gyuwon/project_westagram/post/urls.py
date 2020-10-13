from django.urls import path
from post.views import CreatePost, GetPost

urlpatterns = [
    path('create', CreatePost.as_view()),
    path('', GetPost.as_view())
]