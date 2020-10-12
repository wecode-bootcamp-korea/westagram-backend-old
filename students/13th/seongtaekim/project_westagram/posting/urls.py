from django.urls    import path
from posting.views  import PostView

urlpatterns = [
    path('write/', PostView.as_view()),
    path('', PostView.as_view())
]