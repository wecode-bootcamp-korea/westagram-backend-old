from django.urls import path
from . import views

app_name = "posting"
urlpatterns = [
    path("comment", views.CommentView.as_view(), name="comment"),
    path("posting", views.PostingView.as_view(), name="posting"),
]
