from django.urls import path
from posting     import views

urlpatterns = [
    path('/create',                                        views.PostCreateView.as_view()),
    path('/read',                                          views.PostReadView.as_view()),                           
    path('/delete/<int:post_id>',                          views.PostDeleteView.as_view()),                         
    
    path('/<int:post_id>/create/comment',                  views.CommentCreateView.as_view()),   
    path('/<int:post_id>/read/comment/<int:comment_id>',   views.CommentReadView.as_view()),     
    path('/<int:post_id>/delete/comment/<int:comment_id>', views.CommentDeleteView.as_view()),     
    
    path('/create/like/<int:post_id>',                     views.PostLikeView.as_view()),           
    path('/read/like//<int:post_id>',                      views.PostLikeView.as_view()),            
    path('/delete/like//<int:post_id>',                    views.PostLikeView.as_view()),           

]
