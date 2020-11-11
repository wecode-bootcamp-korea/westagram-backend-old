from django.urls    import path
from .views         import Post, Comment

urlpatterns =[
    path('post/',Post.as_view()),
    path('comment/',Comment.as_view()),
]
