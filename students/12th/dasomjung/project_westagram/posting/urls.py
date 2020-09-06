from django.urls import path
from .           import views

app_name = 'posting'

urlpatterns = [
    path('registerpost', views.RegisterPost.as_view(), name='registerpost'),
    path('posting', views.Posting.as_view(), name='posting'),
]