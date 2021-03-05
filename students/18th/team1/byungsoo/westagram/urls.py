from django.urls import path, include

urlpatterns = [
    path('westagram', include('user.urls'))
]
