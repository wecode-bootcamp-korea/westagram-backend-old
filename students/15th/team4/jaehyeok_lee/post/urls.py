from django.urls import path

from . import views

urlpatterns = [
    path('upload', views.Upload.as_view()),
    path('load', views.Load.as_view()),
    path('writecomment', views.WriteComment.as_view()),
    path('readcomment', views.ReadComment.as_view()),
]
