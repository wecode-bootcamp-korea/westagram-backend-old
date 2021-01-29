from django.urls import path
from user.views import UserView

urlpatterns = [
        path('/signup', UserView.as_view()),

]
