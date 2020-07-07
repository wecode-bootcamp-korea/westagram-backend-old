from django.urls import path

from .views import *

urlpatterns = [
    path('', PostingView.as_view()),
    path('comment/', CommentView.as_view())
]
