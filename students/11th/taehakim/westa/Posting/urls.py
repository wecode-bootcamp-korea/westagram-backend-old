from django.urls import path
from . views import EnrollPost
from . views import ViewGet
from . views import EnrollComment
from . views import ViewComment

urlpatterns = [

  path('enroll_post', EnrollPost.as_view()),
  path('view_get', ViewGet.as_view()),
  path('enroll_comment', EnrollComment.as_view()),
  path('view_comment', ViewComment.as_view())
]