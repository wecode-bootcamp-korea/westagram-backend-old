from django.urls import path

from posting.views import PostingView, GetArticlesView

urlpatterns = [
    path('/posting', PostingView.as_view()),
    path('/articles', GetArticlesView.as_view()) 
]
