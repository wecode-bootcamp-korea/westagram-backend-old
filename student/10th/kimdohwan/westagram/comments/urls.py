from django.urls import path
from . import views

app_name = "comment"

urlpatterns = [
    path("comment", views.CommentView.as_view(), name="comment"),
]
