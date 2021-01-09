from django.urls import path
from posting     import views

urlpatterns = [
    path('/create',                  views.PostCreateView.as_view()),
    path('/read',                    views.PostReadView.as_view()),                           
    path('/delete/<int:pk>',         views.PostDeleteView.as_view()),                         
    
    path('/create/<int:pk>/comment', views.PostCommentView.as_view()),   
    path('/read/<int:pk>/comment',   views.PostCommentView.as_view()),     
    path('/delete/<int:pk>/comment', views.PostCommentView.as_view()),     
    
    path('/create/<int:pk>/like',    views.PostLikeView.as_view()),           
    path('/read/<int:pk>/like',      views.PostLikeView.as_view()),            
    path('/delete/<int:pk>/like',    views.PostLikeView.as_view()),           

]
