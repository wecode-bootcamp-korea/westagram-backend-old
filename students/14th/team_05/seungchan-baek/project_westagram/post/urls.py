from django.urls import path

from .views import CreateView, ReadView, CommentRegister,CommentRead

urlpatterns = [
    path('/create',CreateView.as_view()),
    path('/postread', ReadView.as_view()),
    path('/commentregister',CommentRegister.as_view()),
    path('/commentread',CommentRead.as_view())
]