from django.urls import path
from posting.views import Posting

urlpatterns = [
    path('', Posting.as_view()),
]

