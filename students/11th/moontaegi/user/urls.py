from django.urls import path
from .views      import SignUpView

urlpatterns = [
    path('', SignUpView.as_view()),
]