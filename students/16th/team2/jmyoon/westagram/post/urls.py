from django.urls import path
from post.views  import PostView, GetView

urlpatterns = [
    path('/upload', PostView.as_view()),
    path('/show'  , GetView.as_view()),
    
]