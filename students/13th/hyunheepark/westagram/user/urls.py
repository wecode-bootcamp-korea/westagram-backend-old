from django.urls import path
from user.views  import SignUpView
from . import views

urlpatterns=[

        path('',views.IndexView),
        path('up/',SignUpView.as_view())
        ]
