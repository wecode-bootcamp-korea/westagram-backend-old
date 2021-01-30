from django.urls import path, include

from user.views import AccountView

urlpatterns = [
    path('', AccountView.as_view())
]
