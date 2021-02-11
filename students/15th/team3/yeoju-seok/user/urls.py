from django.urls import path,include
from .views import AccountView,LoginView


urlpatterns = [
    path('/account', AccountView.as_view()),
    path('/login', LoginView.as_view())
]

