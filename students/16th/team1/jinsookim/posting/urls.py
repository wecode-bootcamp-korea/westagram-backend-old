from django.urls import path
from posting.views import Post
urlpatterns = [
    path('/register', Post.as_view()),
    
]