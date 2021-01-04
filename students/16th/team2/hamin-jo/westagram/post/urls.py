from django.urls import path

from post.views import PostView

urlpatterns=[
    path('', PostView.as_view())
]