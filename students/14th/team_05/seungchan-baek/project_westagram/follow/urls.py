from django.urls import path

from .views      import FollowingView

urlpatterns=[
    path('/following',FollowingView.as_view())
]