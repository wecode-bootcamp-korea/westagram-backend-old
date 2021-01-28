from django.urls    import path
from user.views     import SignupView, LogInView

urlpatterns=[
    path('/signup', SignupView.as_view()),
    path('/login', LogInView.as_view())
]