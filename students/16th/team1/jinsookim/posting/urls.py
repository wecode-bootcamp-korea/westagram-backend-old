from django.urls import path
from posting.views import (Post,
                           Comment,
                           UpdateView,
                           Love_Function,
                           Post_Delete_View,
                           Comment_Delete_View,
                           CommentsInCommentsView)

urlpatterns = [
    path('/register', Post.as_view()),
    path('/<int:post_id>', Comment.as_view()),
    path('/love/<int:post_id>', Love_Function.as_view()),
    path('/delete_post/<int:post_id>', Post_Delete_View.as_view()),
    path('/delete_comment/<int:post_id>/<int:comment_id>', Comment_Delete_View.as_view()),
    path('/update/<int:post_id>', UpdateView.as_view()),
    path('/commentsincomments/<int:post_id>/<int:comment_id>', CommentsInCommentsView.as_view())
]



