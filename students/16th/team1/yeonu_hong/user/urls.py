from django.urls import path
from .views      import SignUpSignInView

urlpatterns = [
    path('',SignUpSignInView.as_view())
]