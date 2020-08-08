from django.urls import path
from .views import AccountView

urlpatterns = [
    path('sign_up',AccountView.as_view())
 ]