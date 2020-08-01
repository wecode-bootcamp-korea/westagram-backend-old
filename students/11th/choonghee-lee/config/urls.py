from django.urls import path, include

urlpatterns = [
    path('register/', include('account.urls'))
]
