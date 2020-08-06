from django.urls import path

from . views import PostView

urlpatterns = [
    path('Post', PostView.as_view())
]
