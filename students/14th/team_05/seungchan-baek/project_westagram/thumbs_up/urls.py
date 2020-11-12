from django.urls import path
from .views     import ThumbsUpView

urlpatterns =[
    path('/thumbs_up',ThumbsUpView.as_view())
]