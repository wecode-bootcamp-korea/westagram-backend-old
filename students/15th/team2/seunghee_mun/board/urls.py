from django.urls import path
from board.views import BoardView

urlpatterns = [
        path('', BoardView.as_view())
]
