
from django.urls import path
from .views import SignUpView, LoginView 


urlpatterns = [
	path('',SignUpView.as_view()),
	path('sign-up/',SignUpView.as_view()),
	path('sign-in/',LoginView.as_view()),
#	path('comment/',CommentView.as_view()),
]
