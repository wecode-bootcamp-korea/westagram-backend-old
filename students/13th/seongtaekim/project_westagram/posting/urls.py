from django.urls    import path
from posting.views  import PostView, CommentView

urlpatterns = [
    path('write/', PostView.as_view()),
    path('comment/', PostView.as_view()),
    path('<int:post_id>/', CommentView.as_view())
]