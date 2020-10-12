from django.urls import path
from account.views import register_account

urlpatterns = [
	path('register/', views.register_account)   
]