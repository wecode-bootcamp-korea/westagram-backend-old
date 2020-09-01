from django.urls import include, path

urlpatterns = [
    path('account/', include('account.urls'))
]
