from django.urls import path
from .views      import ContentSignUpView, ContentGetView

urlpatterns = [
    path('/contentsignup', ContentSignUpView.as_view()),
    path('/contentget', ContentGetView.as_view())
]