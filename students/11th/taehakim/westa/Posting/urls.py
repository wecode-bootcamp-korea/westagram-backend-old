from django.urls import path
from . views import EnrollPost
from . views import ViewGet

urlpatterns = [

  path('enroll_post', EnrollPost.as_view()),
  path('view_get', ViewGet.as_view())
]