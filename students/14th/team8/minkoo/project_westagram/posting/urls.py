from django.urls import path

from .views import PostsView

urlpatterns = [
    path('', PostsView.as_view(), name='post')
]
