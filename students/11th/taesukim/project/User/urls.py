from django.urls import path

from .views import SingUpView

urlpatterns = [
	path('', SingUpView.as_view())
]
