from django.urls import path
from .views import Post

urlpatterns = [
    path('', PostView.as_view())
]