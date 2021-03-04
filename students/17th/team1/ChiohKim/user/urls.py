from django.urls import path
from . views    import SignupView, LoginView

urlpatterns = [
        path('/SignupView', SignupView.as_view()),
        path('/LoginView', LoginView.as_view()),
]
