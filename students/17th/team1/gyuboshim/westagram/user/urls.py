from django.urls    import path, include
from .views         import UserView, LoginView

urlpatterns = [
    path('/signup', UserView.as_view()),
    path('/signin', LoginView.as_view())
]
