from django.urls import path
from .views      import ContentSignupView, ContentGetView, UserCommentView, GetCommentView

urlpatterns = [
       path('/post', ContentSignupView.as_view()),
       path('/get', ContentGetView.as_view()),
       path('/commentpost', UserCommentView.as_view()),
       path('/getpost', GetCommentView.as_view())
    ]
