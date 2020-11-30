from django.urls import path
from .views import AccountsView, LoginView

urlpatterns = {
    path("", AccountsView.as_view()),
    path("/log-in", LoginView.as_view())
}

