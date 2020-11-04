from django.urls import path, include

urlpatterns = [
    path('sign', include('account.urls')),
]
