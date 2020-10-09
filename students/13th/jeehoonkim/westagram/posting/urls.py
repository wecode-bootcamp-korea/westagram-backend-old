from django.urls import path
from .views import PostingView

urlpatterns = [
    path('', PostingView.as_view()),
    path('create', PostingView.as_view()),   
]