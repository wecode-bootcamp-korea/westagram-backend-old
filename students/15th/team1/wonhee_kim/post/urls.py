from django.urls import path

from .views import post_views


urlpatterns = [
    path('/create/post', post_views.CreatePostView.as_view()),
    path('/read/post', post_views.ReadPostView.as_view()),
]