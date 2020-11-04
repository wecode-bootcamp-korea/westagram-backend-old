from django.urls import path, include

urlpatterns = [
        path('user/', include('user.urls')),
        path('posts/', include('posts.urls'))
]
