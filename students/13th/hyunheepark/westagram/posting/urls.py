from django.urls   import path
from posting.views import PostView

urlpatterns = [
        path('',PostView.as_view())
        ]
