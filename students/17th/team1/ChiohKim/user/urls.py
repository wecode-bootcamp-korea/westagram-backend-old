from django.urls import path
from . views    import SignupView

urlpatterns = [
        path('', SignupView.as_view()),
        ]
