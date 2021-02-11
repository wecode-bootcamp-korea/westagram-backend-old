from django.urls import path, include
from like.views  import LikeView

urlpatterns = [
    path('', LikeView.as_view()),
]