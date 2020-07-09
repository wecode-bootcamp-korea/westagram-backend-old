from django.urls import path
from .views  import MainView, SignIn, Comment


urlpatterns = [
	path('', MainView.as_view()),
	path('signin/', SignIn.as_view()),
	path('comment/', Comment.as_view())
]
