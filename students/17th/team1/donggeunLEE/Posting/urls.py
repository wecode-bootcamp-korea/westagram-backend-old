from django.urls import path
from .views      import (ContentSignupView, 
        ContentGetView, 
        UserCommentView, 
        AddCommentView 
        )

urlpatterns = [
       path('/post', ContentSignupView.as_view()),
       path('/get', ContentGetView.as_view()),
       path('/commentpost', UserCommentView.as_view()),
       path('/add', AddCommentView.as_view()),
       #path('/like', UserLikeView.as_view())
    ]
