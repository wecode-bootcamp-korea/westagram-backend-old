from django.urls import path
from django.urls import include, path

urlpatterns = [
    path('user/', include('user.urls')),
]