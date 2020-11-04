from django.urls import path

from .views      import SignUpView, SignInView, FollowPost, FollowGet

urlpatterns = [
	path('signup', SignUpView.as_view()),
    path('signin', SignInView.as_view()),
    path('followpost', FollowPost.as_view()),
    path('followget', FollowGet.as_view()),
]
