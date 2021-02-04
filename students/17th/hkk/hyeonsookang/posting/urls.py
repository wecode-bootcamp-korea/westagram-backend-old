
from django.urls import path
from posting.views import PostView

urlpatterns = [
        path('/posting', PostView.as_view()),
        ]
