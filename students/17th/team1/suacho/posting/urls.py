from django.urls import path
from .views import PostingView

urlpatterns = [
        path('', PostingView.as_view()),
]
