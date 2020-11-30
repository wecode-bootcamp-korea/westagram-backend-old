from django.urls import path

from .views      import FollowingView,DeleteFollowView

urlpatterns=[
    path('/following',FollowingView.as_view()),
    path('/delete', DeleteFollowView.as_view())
]