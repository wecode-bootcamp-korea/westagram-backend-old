from django.urls import path

from posting.views import PostingView

urlpatterns = [
    path('/posting', PostingView.as_view())
] # just example
