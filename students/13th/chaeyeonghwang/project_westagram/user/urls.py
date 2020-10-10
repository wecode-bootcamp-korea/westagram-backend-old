from user.views import SignupView, LoginView

urlpatterns = [
    path('user/signin', SignupView.as_view()),
    path('user/login', LoginView.as_view())
]
