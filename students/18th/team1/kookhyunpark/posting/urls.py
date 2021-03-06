from django.urls import path

from posting.views import PostUploadView

urlpatterns = [
    path('/upload', PostUploadView.as_view())
]