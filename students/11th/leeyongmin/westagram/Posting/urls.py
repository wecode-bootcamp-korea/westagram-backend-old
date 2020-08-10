from django.urls import path
from . import views

app_name='Posting'

urlpatterns = [
    path('upload', views.Upload.as_view()),
    path('show', views.Show.as_view())
]
