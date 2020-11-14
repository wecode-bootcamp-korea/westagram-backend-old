from django.urls    import path
from .views         import Post, Comment, Like

urlpatterns =[
    path('post/',Post.as_view()),
    path('comment/',Comment.as_view()),
    path('like/',Like.as_view()),
]
