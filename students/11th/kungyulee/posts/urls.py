from django.urls import path

from .views import PostView,PostListView 

urlpatterns = [
    path('create', PostView.as_view()),
    path('list', PostListView.as_view()),
]
