from django.urls  import path
from posting.views  import Posting

urlpatterns =  [
    path ('/posting' , Posting.as_view()),
]


