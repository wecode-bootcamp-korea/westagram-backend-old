from django.urls import path, include
#from user.views      import SignUpView, LogInView

urlpatterns = [
     path('user', include('user.urls')),
     path('posting' , include('posting.urls')) ,


]
