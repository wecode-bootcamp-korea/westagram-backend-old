from django.urls import path
from .views import PostView, DisplayPostView

urlpatterns = [
    path('post/', PostView.as_view()),
    path('displaypost/', DisplayPostView.as_view())
]
