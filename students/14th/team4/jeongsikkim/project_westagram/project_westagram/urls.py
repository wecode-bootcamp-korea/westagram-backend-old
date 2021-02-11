from django.urls import path, include

urlpatterns = [
    path('user', include('user.urls')),
    path('posting', include('posting.urls'))
]
