from django.urls import path
from .views import MainView, Signin, Comment

urlpatterns = [
	path('signup/', MainView.as_view(), name='signup'),
	path('signin/', Signin.as_view(), name='signin'),
	path('comment/', Comment.as_view(), name='comment'),	
]
