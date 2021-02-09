from django.urls import path
from user.views import SignInView
from user.views import SignUpView
from user.views import RelationShipView
from user.views import RelationShipUnfollowView

urlpatterns = [
    path('', SignUpView.as_view()),
    path('/login', SignInView.as_view()),
    path('/relationship/<int:to_user_id>/follow', RelationShipView.as_view()),
    path('/relationship/<int:to_user_id>/unfollow', RelationShipUnfollowView.as_view()),
]


