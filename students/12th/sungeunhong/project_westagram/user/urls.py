from django.urls import path
from .views import AccountView

urlpatterns = [
    path('accout', AccountView.as_view()),
    # path('login', loginView.as_view()),
]