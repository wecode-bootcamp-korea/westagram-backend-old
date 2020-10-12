from django.urls import path
from . import views

urlpatterns = [
    path('article/', views.Post.as_view()),
    path('comment/', views.Comment.as_view()),
    path('like/', views.Like.as_view()),
    path('follow/', views.Follow.as_view()),
]
