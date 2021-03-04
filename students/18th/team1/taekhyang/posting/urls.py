from django.urls import path, include

from .views import UploadView


urlpatterns = [
    path('/upload', UploadView.as_view())  
]
