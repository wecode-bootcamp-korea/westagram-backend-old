from django.urls import path

from . import views

urlpatterns = [
    path('', views.LikeView.as_view()),
]
