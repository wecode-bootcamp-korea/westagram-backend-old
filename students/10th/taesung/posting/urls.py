from django.urls import path
from .views import post

urlpatterns = [
        path('', post.as_view())
        ]
