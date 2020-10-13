from django.urls import path
from account.views import RegisterView

urlpatterns = [
	path('', RegisterView.as_view())
]