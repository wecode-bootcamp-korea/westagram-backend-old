from django.urls   import path
from .views        import UserSignInView, UserSignUpView

urlpatterns = [
    path('/SignUp', UserSignUpView.as_view()),
    path('/SignIn', UserSignInView.as_view())
    ]
