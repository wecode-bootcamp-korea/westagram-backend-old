from django.urls import  path
from .views import UsersView

urlpatterns = [
    path('', UsersView.as_view())
]
