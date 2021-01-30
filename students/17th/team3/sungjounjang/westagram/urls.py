from django.urls import path, include

urlpatterns = [
    path('account', include('user.urls'))
]
