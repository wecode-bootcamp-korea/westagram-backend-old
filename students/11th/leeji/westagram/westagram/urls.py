from django.urls import path, include

urlpatterns = [
    path('sign', include('user.urls')),
    path('post', include('posting.urls')),
]