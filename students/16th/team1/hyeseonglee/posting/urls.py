from django.urls import path
from posting.views  import PostView

urlpatterns = [
    path('/create', PostView.as_view()),
    path('/read', PostView.as_view()),
]
