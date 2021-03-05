from django.urls import path
from .views      import PostManage, ReplyManage

urlpatterns = [
    path('', PostManage.as_view()),
    path('/reply', ReplyManage.as_view())
]