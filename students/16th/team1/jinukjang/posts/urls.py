from django.urls import path
from .views      import CreatePostView, ReadPostView

urlpatterns = [
    path('/create',CreatePostView.as_view()),
    path('/read'  ,ReadPostView.as_view())
]