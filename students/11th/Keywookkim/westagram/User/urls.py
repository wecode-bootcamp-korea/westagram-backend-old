from django.urls              import path
from .views                   import Signup, Login

urlpatterns = [
    path('signuplist', Signup.as_view()),
    path('login', Login.as_view())
    #url(r'^api-token-auth/', views.obtain_auth_token)
]
