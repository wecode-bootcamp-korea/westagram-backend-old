from django.urls import path
from .views      import FollowView

urlpatterns = [
    path('/follow', FollowView.as_view()),
]