from django.urls    import path

from .views         import PostingView, ReadPostingView

urlpatterns = [
    path('/create', PostingView.as_view()),
    path('/read',   ReadPostingView.as_view())
]
