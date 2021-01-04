from django.urls import path
from .views      import SignUpSignInView#, FollowView

urlpatterns = [
    path('',SignUpSignInView.as_view()),
    #path('<int:user_id>/', FollowView.as_view())
]