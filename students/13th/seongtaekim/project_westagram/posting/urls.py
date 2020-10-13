from django.urls    import path
from posting.views  import PostView, CommentView, LikeView

urlpatterns = [
    path('write/', PostView.as_view()),
    path('', PostView.as_view()),
    path('like/', LikeView.as_view()),
    path('comment/', PostView.as_view()),
    path('<int:post_id>/', CommentView.as_view())
]