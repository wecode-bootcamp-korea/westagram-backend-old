from django.urls import path
from user.views import UsersView

urlpatterns=[
    path('', UsersView.as_view())
]