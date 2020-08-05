from django.urls import path, include

urlpatterns = [
    path('user/',include('User.urls')),
    path('posting/', include('Posting.urls'))
]

