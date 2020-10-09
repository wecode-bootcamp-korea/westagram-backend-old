from django.urls import path
from .views import PostingView

urlpatterns = [
    path('create', PostingView.as_view()),
]