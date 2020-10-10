from django.urls import path
from posting.views  import CreatePost, PostView

urlpatterns = [
    path('', PostView.as_view()),
    path('create', CreatePost.as_view())
]