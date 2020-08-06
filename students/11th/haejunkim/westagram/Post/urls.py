from django.urls import path

from .views import PostView, PostDisplayView

urlpatterns = [
    path('post', PostView.as_view()),
    path('postdisplay', PostDisplayView.as_view()),
]
