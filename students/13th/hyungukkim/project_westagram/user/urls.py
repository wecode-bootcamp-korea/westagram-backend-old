from django.urls import path

from user.views import SignUpView, SignInView, FollowAccount

urlpatterns = [
	path('signup', SignUpView.as_view()),
	path('signin', SignInView.as_view()),
	path('follow_account', FollowAccount.as_view())
]
