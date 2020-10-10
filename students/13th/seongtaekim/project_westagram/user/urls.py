from django.urls import path
from user.views  import Loginview

urlpatterns = [
    path('signup/', Loginview.as_view(), name='login'),
]