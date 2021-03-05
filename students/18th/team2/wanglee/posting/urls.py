from django.urls import path
from .views      import PostManage, ReplyManage, LikeManage

urlpatterns = [
    path('', PostManage.as_view()),
    path('/reply', ReplyManage.as_view()),
    path('/like', LikeManage.as_view())
]