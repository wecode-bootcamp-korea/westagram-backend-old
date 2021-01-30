from django.urls import path

from user.views import AccountView

urlpatterns = [
    path('', AccountView.as_view())
]
