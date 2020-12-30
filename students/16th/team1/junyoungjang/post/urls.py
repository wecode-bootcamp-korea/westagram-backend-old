from django.urls import path

from .views import PostCreateView, PostReadView

urlpatterns = [
    path('/create', PostCreateView.as_view()), 
    path('/read', PostReadView.as_view()),
]