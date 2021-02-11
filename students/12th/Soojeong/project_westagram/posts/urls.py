from django.urls import path
from .views import PostingView

app_name="posts"

urlpatterns = [
        path('posting', PostingView.as_view()),        
]