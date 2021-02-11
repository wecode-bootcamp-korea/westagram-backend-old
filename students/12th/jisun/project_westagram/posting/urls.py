from django.urls import path

from .           import views

app_name = 'posting'
urlpatterns = [
        path('', views.RegisterView.as_view(), name = 'content'),
        path('comment/<int:image_url_id>', views.CommentView.as_view(), name = 'comment')
        ]
