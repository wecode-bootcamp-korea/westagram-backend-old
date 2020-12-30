from django.urls import path,include
from user.views  import SignUpView

urlpatterns = [
    path('', SignUpView.as_view()),
]
