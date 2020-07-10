from django.contrib import admin
from django.urls    import path,include

urlpatterns = [
    path('user',include('users.urls')),
    path('post',include('posts.urls')),
]
