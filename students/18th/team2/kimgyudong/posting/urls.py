from django.urls import path

from .views import Posting

urlpatterns = [
   path('/post', Posting.as_view()),
]
