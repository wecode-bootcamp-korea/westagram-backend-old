from django.urls import path
from .views      import ContentSignupView, ContentGetView

urlpatterns = [
       path('/post', ContentSignupView.as_view()),
       path('/get', ContentGetView.as_view())
    ]
