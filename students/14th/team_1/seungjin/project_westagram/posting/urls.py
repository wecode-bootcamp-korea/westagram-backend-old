from django.urls import path
from .views import (
                    Posting, 
                    ShowAllPosts,
                    AddComment,
                    ShowAllComments,
                    ShowCommentsOfContent, 
                    AddLike,
                    )

urlpatterns = [
        path('/regist',                     Posting.as_view()),
        path('/show_all_posts',             ShowAllPosts.as_view()),        
        path('/add_comment',                AddComment.as_view()),        
        path('/show_all_comments',          ShowAllComments.as_view()),  
        path('/show_comments_of_content',   ShowCommentsOfContent.as_view()),
        path('/add_like',                   AddLike.as_view()),
        ]
