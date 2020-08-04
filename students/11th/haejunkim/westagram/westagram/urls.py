from django.urls import path , include

urlpatterns = [
    path('User', include('User.urls')),
]
