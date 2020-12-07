from django.urls    import path
from users.views import SignUpView, SignInView

urlpatterns = [
    path('/sign_up', SignUpView.as_view()),
    path('/sign_in', SignInView.as_view()),
]
