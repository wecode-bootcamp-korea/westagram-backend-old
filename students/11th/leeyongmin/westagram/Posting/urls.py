from django.urls import path
from . import views

app_name='Posting'

urlpatterns = [
    path('uploadpost', views.UploadPost.as_view()),
    path('showpost', views.ShowPost.as_view()),
    path('uploadcomment', views.UploadComment.as_view()),
    path('showcomment', views.ShowComment.as_view())
]
