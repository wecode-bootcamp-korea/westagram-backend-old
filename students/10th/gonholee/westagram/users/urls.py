from django.urls    import path

from .              import views

urlpatterns = [
    path('/sign-up',views.SignUpView.as_view()),
    path('/sign-in',views.SignInView.as_view()),
    path('/follow-user',views.FollowUserView.as_view()),
]

