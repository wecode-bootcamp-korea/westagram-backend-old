from django.urls import path
from posting.views import Posting, Comment

urlpatterns = [
    path('', Posting.as_view()),
    path('/comment', Comment.as_view()),
]

