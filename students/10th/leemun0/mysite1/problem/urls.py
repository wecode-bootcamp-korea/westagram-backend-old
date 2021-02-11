
from django.urls import path
from .views import MainView, LoginView


urlpatterns = [
	path('',MainView.as_view()),
	path('sign-up/',MainView.as_view()),
	path('sign-in/',LoginView.as_view()),
]
