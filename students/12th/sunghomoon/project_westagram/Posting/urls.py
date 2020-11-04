from django.urls import path
from Posting.views  import postRegister, postGet

app_name = 'Posting'

urlpatterns = [
    path('postRegister/', postRegister.as_view()),
    path('postGet/', postGet.as_view())
]
