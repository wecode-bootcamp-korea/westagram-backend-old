from django.urls    import path, include
from .views         import PostView, PostDisplayView

urlpatterns = [
    path('post', PostView.as_view()),
    path('postdisplayview', PostDisplayView.as_view())
]
