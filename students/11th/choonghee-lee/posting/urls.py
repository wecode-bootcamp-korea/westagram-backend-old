from django.urls import path

from .views import CreatePostView, ListPostView

app_name = 'posting'

urlpatterns = [
    path('create/', CreatePostView.as_view(), name="create"),
    path('list/', ListPostView.as_view(), name="list")
]