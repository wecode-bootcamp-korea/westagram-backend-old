from django.urls import path
from .views import RegisterView, ExpressView

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('express/',ExpressView.as_view()),
]
