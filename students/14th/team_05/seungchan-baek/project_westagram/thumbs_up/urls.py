from django.urls import path
from .views     import ThumbsUpView,DeleteLikeView

urlpatterns =[
    path('/thumbs_up',ThumbsUpView.as_view()),
    path('/delete', DeleteLikeView.as_view())
]