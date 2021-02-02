from django.urls import path
from .views      import CreatePostView

urlpatterns = [
    path('/createpost', CreatePostView.as_view()),
]