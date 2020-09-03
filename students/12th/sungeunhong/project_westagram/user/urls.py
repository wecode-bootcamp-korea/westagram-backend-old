from django.urls import path
from .views import AccountView

urlpatterns = [
    path('account', AccountView.as_view()),
    # path('login', loginView.as_view()),
]

#localhost:8000/user/account