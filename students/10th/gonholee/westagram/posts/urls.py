from django.urls    import path
from .              import views

urlpatterns = [
    path('', views.PostRegister.as_view()),
    path('comment-regist', views.CommentRegister.as_view()),
    path('post-like/', views.PostLike.as_view()),
]
