from django.urls import path
from .views import Posting

urlpatterns = [
    path('/posting', Posting.as_view()),

]