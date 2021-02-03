from django.urls import path

from .views      import PostingView

urlpatterns = [
    path('/post', PostingView.as_view()) ## name?  ##as_view() is coming from View... inheritance. 
    
]
